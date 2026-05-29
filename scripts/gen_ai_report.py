#!/usr/bin/env python3
"""Generate AI analyst reports from a stock queue (batch 5 per run).

Usage:
    python3 scripts/gen_ai_report.py              # Generate next 5 reports
    python3 scripts/gen_ai_report.py --list       # Show queue status
    python3 scripts/gen_ai_report.py --reset      # Mark all as not generated
    python3 scripts/gen_ai_report.py --company 中芯国际  # Single company by name

Requires env vars:
    MCP_URL       = DashScope MCP endpoint
    MCP_TOKEN     = Bearer token for MCP auth
    DEEPSEEK_KEY  = DeepSeek API key
"""

import json, os, sys, re, time, argparse, textwrap
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import urllib.request, urllib.error

BASE = Path(__file__).resolve().parent.parent
QUEUE_FILE = BASE / 'data' / 'stock-queue.json'
PROGRESS_FILE = BASE / 'data' / 'stock-progress.json'
ARTICLES_CN = BASE / 'articles.json'
ARTICLES_EN = BASE / 'en' / 'articles.json'
INDEX_CN = BASE / 'ai-analyst' / 'index.html'
INDEX_EN = BASE / 'en' / 'ai-analyst' / 'index.html'
REPORTS_CN_DIR = BASE / 'ai-analyst'
REPORTS_EN_DIR = BASE / 'en' / 'ai-analyst'
TODAY = datetime.now(timezone.utc).strftime('%Y-%m-%d')

MCP_URL = os.environ.get('MCP_URL', '')
MCP_TOKEN = os.environ.get('MCP_TOKEN', '')
DEEPSEEK_KEY = os.environ.get('DEEPSEEK_KEY', '')
BATCH_SIZE = 5


# ═══════════════════════════════ MCP Client ═══════════════════════════════

def mcp_call(tool, args):
    """Call MCP tool via JSON-RPC 2.0 streamableHttp."""
    payload = json.dumps({
        'jsonrpc': '2.0', 'id': 1,
        'method': 'tools/call',
        'params': {'name': tool, 'arguments': args},
    }).encode()
    req = urllib.request.Request(
        MCP_URL,
        data=payload,
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {MCP_TOKEN}'},
    )
    resp = urllib.request.urlopen(req, timeout=60)
    d = json.loads(resp.read().decode())
    if d.get('error'):
        raise Exception(f'MCP error: {d["error"]["message"]}')
    text = d.get('result', {}).get('content', [{}])[0].get('text', '')
    if not text:
        raise Exception(f'Empty MCP response for: {tool}')
    parsed = json.loads(text)
    # Unwrap { code, data, message } envelope
    if isinstance(parsed, dict) and 'code' in parsed and 'data' in parsed:
        return parsed['data']
    return parsed


def mcp_extract_rows(data):
    """Extract array from MCP response."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ('data', 'list', 'records', 'items'):
            val = data.get(key)
            if isinstance(val, list):
                return val
    return []


def search_stock(name):
    return mcp_call('search', {'key': name, 'type': '11', 'pageSize': 5})


def get_basic_info(code):
    return mcp_call('get_stock_basic_info', {'stockCode': code})


def get_income(code, begin='2021-01-01', end='2026-12-31'):
    return mcp_call('list_stock_income_statements', {
        'stockCodes': [code], 'beginDate': begin, 'endDate': end, 'pageSize': 500,
    })


def get_balance_sheet(code):
    return mcp_call('list_stock_balance_sheet', {'stockCodes': [code], 'pageSize': 500})


def get_cash_flow(code, begin='2025-01-01', end='2026-12-31'):
    return mcp_call('list_stock_cash_flows', {
        'stockCode': code, 'beginDate': begin, 'endDate': end, 'pageSize': 500,
    })


def get_quotes(code, begin='2025-05-01', end=TODAY):
    return mcp_call('list_stock_adjusted_quotes', {
        'stockCodes': [code], 'beginDate': begin, 'endDate': end, 'pageSize': 500,
    })


# ═══════════════════════════════ DeepSeek Client ═══════════════════════════════

DEEPSEEK_SYSTEM_PROMPT = textwrap.dedent("""\
你是一位资深买方分析师。请严格按照要求输出。

## 输出要求（极其重要）
你必须只输出一个合法JSON对象。不要输出任何其他文字、不要用markdown代码块包裹、不要加解释、不要加前后缀。
直接以 { 开头，以 } 结尾。

## JSON结构
{
  "subtitle": "一句话副标题，10-20字，类似「AI算力霸主的芯片帝国」「高股息银行股的估值修复之路」，提炼公司核心投资逻辑",
  "executive_summary": "三段核心摘要（每段含核心**数字**），每段3-4句，用\\\\n\\\\n分隔",
  "sections": [
    { "id": "s1", "title": "一、公司概况", "content": "使用 Markdown 格式的500-800字分析" },
    { "id": "s2", "title": "二、财务分析", "content": "..." },
    { "id": "s3", "title": "三、技术分析", "content": "..." },
    { "id": "s4", "title": "四、市场情绪", "content": "..." },
    { "id": "s5", "title": "五、竞品对比", "content": "..." },
    { "id": "s6", "title": "六、估值与财务健康度", "content": "..." },
    { "id": "s7", "title": "七、主要风险", "content": "..." },
    { "id": "s8", "title": "八、结论与建议", "content": "..." }
  ]
}

## Markdown 格式要求（极其重要）
每个 section 的 content 字段必须使用以下 Markdown 语法：

### 子标题（每个章节至少2个）
每章必须用 ### 做内容分层，至少2个，建议3-4个。
例如财务分析章：### 2.1 营收趋势\\n### 2.2 盈利能力\\n### 2.3 资产质量
技术分析章：### 3.1 价格走势\\n### 3.2 技术指标\\n### 3.3 支撑位与阻力位

### 加粗
所有关键数字用 **数字+单位** 包裹，如**营收1788亿元**、**净利润610亿元**、**毛利率34%**

### 列表（每个章节至少1个）
- 用 - item 枚举业务板块、竞争优势、数据要点
- 每个要点包含具体数值
- 每个章节至少使用1个列表

### 编号列表
1. 用 1. 2. 3. 等列举风险因素、壁垒、步骤
2. 每项包含机制描述和影响程度

### 表格（特别重要）
竞品对比章（s5）和估值章（s6）必须各含至少一个对比表格：
| 指标 | 公司A | 公司B | 公司C |
|------|-------|-------|-------|
| 营收 | **XX** | **XX** | **XX** |
对比表格放在章节末尾。

### 段落
- 段落之间空行分隔
- 每段4-6句话，包含数据支撑
- 避免短的段落

## 写作准则
- 语言专业、客观、数据驱动
- 不编造数字，引用的数据必须来自用户提供的输入
- **禁止输出"数据缺失"、"暂缺"、"未提供"等弱化语气**——直接跳过无数据内容
- 每章节500-800字，有深度分析
- 全篇总字数6000-8000字
- 用中文
- 行之间用换行符\\n分隔

## 8段内容指引（每段至少2个###子标题）
1. **公司概况**：###分业务板块（3-4个用列表）、竞争壁垒（编号列表）、市场地位（数据支撑）
2. **财务分析**：###分营收趋势（含同比增速）、盈利能力（毛利率/净利率）、费用控制、资产质量（资产负债率/ROE）；每子节用列表枚举关键**数字**
3. **技术分析**：###分价格走势（52周区间）、技术指标（RSI/MACD/KDJ）、均线系统（MA20/MA60/MA120）；列举关键价位
4. **市场情绪**：###分布研报评级（卖方覆盖）、资金流向（主力/散户）、机构持仓变化
5. **竞品对比**：###分行业格局（段落分析）、各公司对比（数据驱动）；末尾必须加对比表格（4-5个指标×3-4家公司）
6. **估值与健康度**：###分估值分析（PE/PB/PEG百分位对比行业）、财务健康度（流动比率/速动比率/资产负债率）；末尾加健康度评分表
7. **主要风险**：###分行业风险、竞争风险、政策风险、技术风险；每类用编号列表写2-3个具体风险
8. **结论与建议**：###分核心观点（段落）、短期建议0-6月（列表写目标价和催化剂）、长期建议6-18月（列表写目标价和逻辑）""")


def deepseek_generate(prompt):
    """Call Qwen (DashScope) API and return parsed JSON report."""
    payload = json.dumps({
        'model': 'qwen-plus',
        'messages': [
            {'role': 'system', 'content': DEEPSEEK_SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.3,
        'max_tokens': 16384,
    }).encode()

    req = urllib.request.Request(
        'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {DEEPSEEK_KEY}',
        },
    )
    resp = urllib.request.urlopen(req, timeout=180)
    d = json.loads(resp.read().decode())
    content = d.get('choices', [{}])[0].get('message', {}).get('content', '')
    if not content:
        raise Exception('Qwen returned empty response')
    return parse_deepseek_json(content)


def parse_deepseek_json(text):
    """Parse JSON from LLM response, handling code fences."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    m = re.search(r'```(?:json)?\s*\n?([\s\S]*?)```', text)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end > start:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass
    raise Exception(f'Could not parse LLM JSON. Response starts: {text[:500]}')


# ═══════════════════════════════ Build Prompt ═══════════════════════════════

def build_prompt(data):
    """Build the prompt with multi-year financial data."""
    lines = []
    lines.append(f'请分析「{data["name"]}」（{data["code"]}）并生成深度研究报告。')
    lines.append('')
    lines.append('## 公司信息')
    lines.append(f'名称：{data["name"]}')
    lines.append(f'股票代码：{data["code"]}')
    lines.append(f'行业：{data.get("industry", "未知")}')
    lines.append(f'市值：{data.get("marketCap", "未知")}')
    lines.append('')

    _latest = data.get('income_rows', [{}])[0] if data.get('income_rows') else {}
    lines.append('## 最新财务数据（最新报告期）')
    lines.append(f'营收：{fmt_num(_latest.get("revenue") or _latest.get("operatingRevenue"))}')
    lines.append(f'净利润：{fmt_num(_latest.get("netProfit") or _latest.get("netIncome"))}')
    lines.append(f'毛利率：{_latest.get("grossProfitMargin", "—")}%' if _latest.get('grossProfitMargin') else '毛利率：—')
    lines.append(f'每股收益：{_latest.get("eps") or _latest.get("basicEps") or "—"}')
    lines.append('')

    years = data.get('years', [])
    rev_data = data.get('rev_data', [])
    profit_data = data.get('profit_data', [])
    margin_data = data.get('margin_data', [])

    if years:
        lines.append('## 历年财务趋势')
        rev_str = ' → '.join(fmt_num(v) if v is not None else '—' for v in rev_data)
        profit_str = ' → '.join(fmt_num(v) if v is not None else '—' for v in profit_data)
        margin_str = ' → '.join(f'{v:.1f}%' if v is not None else '—' for v in margin_data)
        lines.append(f'营收逐年：{rev_str}')
        lines.append(f'净利润逐年：{profit_str}')
        lines.append(f'毛利率逐年：{margin_str}')

        lines.append('')
        lines.append('| 年份 | 营收(万元) | 净利润(万元) | 毛利率 |')
        lines.append('|------|-----------|-------------|-------|')
        for i in range(len(years)):
            r = fmt_num(rev_data[i]) if i < len(rev_data) and rev_data[i] is not None else '—'
            p = fmt_num(profit_data[i]) if i < len(profit_data) and profit_data[i] is not None else '—'
            m = f'{margin_data[i]:.1f}%' if i < len(margin_data) and margin_data[i] is not None else '—'
            lines.append(f'| {years[i]} | {r} | {p} | {m} |')

    if len(rev_data) >= 2 and rev_data[-1] and rev_data[-2] and rev_data[-2] > 0:
        rev_yoy = (rev_data[-1] - rev_data[-2]) / rev_data[-2] * 100
        lines.append(f'\n最新营收同比增速：{rev_yoy:.1f}%')
        if len(profit_data) >= 2 and profit_data[-1] and profit_data[-2] and profit_data[-2] > 0:
            profit_yoy = (profit_data[-1] - profit_data[-2]) / profit_data[-2] * 100
            lines.append(f'最新净利润同比增速：{profit_yoy:.1f}%')

    lines.append('')
    lines.append('## 市场数据')
    price = data.get('price')
    high52 = data.get('high52')
    low52 = data.get('low52')
    pe = data.get('pe')
    pb = data.get('pb')

    if price is not None:
        lines.append(f'最新价：{price:.2f}元')
    if high52 is not None:
        lines.append(f'52周最高：{high52:.2f}元')
    if low52 is not None:
        lines.append(f'52周最低：{low52:.2f}元')
    if pe is not None:
        lines.append(f'PE：{pe:.1f}x')
    if pb is not None:
        lines.append(f'PB：{pb:.2f}x')
    if price is not None and high52 is not None and low52 is not None and high52 > low52:
        pct = (price - low52) / (high52 - low52) * 100
        lines.append(f'价格在52周区间位置：{pct:.0f}%')

    return '\n'.join(lines)


# ═══════════════════════════════ HTML Renderer ═══════════════════════════════

def render_report_cn(data):
    """Render CN report HTML — matches renderer.js output structure."""
    co = escape(str(data.get('company', '') or ''))
    code = escape(str(data.get('code', '') or ''))
    slug = data.get('slug', 'report')
    industry = escape(str(data.get('industry', '') or ''))
    price = data.get('latestPrice')
    pe = data.get('pe')
    pb = data.get('pb')
    high52 = data.get('high52')
    low52 = data.get('low52')
    subtitle = data.get('subtitle', '') or 'AI 深度研究'
    exec_summary = data.get('executive_summary', '')
    sections = data.get('sections', [])
    chart_data = data.get('chart_data', {})
    years = chart_data.get('years', [])
    rev_data = chart_data.get('revenue', [])
    profit_data = chart_data.get('netIncome', [])
    margin_data = chart_data.get('grossMargin', [])
    prices = chart_data.get('prices', [])

    has_margin = any(v is not None for v in (margin_data or []))

    # YoY growth data (rev_data is oldest→latest, compute latest→oldest)
    yoy_labels = years[1:] if len(years) > 1 else []
    yoy_data = []
    for i in range(len(rev_data) - 1):
        if rev_data[i] and rev_data[i] > 0:
            yoy_data.append(round((rev_data[i + 1] - rev_data[i]) / rev_data[i] * 100, 1))
        else:
            yoy_data.append(None)
    has_yoy = len(yoy_data) >= 2

    # Indicator grid data
    pct = None
    if price is not None and high52 is not None and low52 is not None and high52 > low52:
        pct = (price - low52) / (high52 - low52) * 100

    # Section navigation
    num_labels = ['一', '二', '三', '四', '五', '六', '七', '八']
    section_nav = ''
    mobile_options = ''
    section_html = ''

    for i, s in enumerate(sections):
        s_title = s.get('title', '').lstrip('一二三四五六七八、 ')
        s_content = s.get('content', '')

        nav_icon = '<i class="fas fa-circle fa-fw" style="width:16px;color:#2563eb;font-size:.5rem;vertical-align:middle"></i>'
        section_nav += f'<li><a href="#s{i+1}">{nav_icon} {escape(s.get("title", ""))}</a></li>\n'
        mobile_options += f'<option value="s{i+1}">{escape(s.get("title", ""))}</option>\n'

        extra = ''
        if i == 2:  # Technical analysis — add indicator grid + price chart
            extra = indicator_grid_html(price, pe, pb, pct)
            extra += price_chart_html(prices)

        sec_content = parse_markdown(s_content) if s_content else '<p>数据不足，暂无法生成该章节详细分析。</p>'
        section_html += f'''
<h2 id="s{i+1}"><span class="section-num">{num_labels[i] if i < len(num_labels) else ""}</span>{escape(s_title)}</h2>
{extra}
{sec_content}'''

    # Stat grid (top-level)
    stat_cards = ''
    if price is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">最新价</div><div class="stat-value">¥{price:.2f}</div></div>\n'
    if pe is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">PE</div><div class="stat-value">{pe:.1f}x</div></div>\n'
    if pb is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">PB</div><div class="stat-value">{pb:.2f}x</div></div>\n'
    if high52 is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">52周最高</div><div class="stat-value">¥{high52:.2f}</div></div>\n'
    if low52 is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">52周最低</div><div class="stat-value">¥{low52:.2f}</div></div>\n'

    # Income chart
    income_chart = ''
    if len(years) >= 3:
        _iy = json.dumps(years)
        _ir = json.dumps(round_to_billion(rev_data))
        _ip = json.dumps(round_to_billion(profit_data))
        income_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-chart-bar" style="color:#2563eb"></i> 营收与净利润趋势</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartIncome"></canvas></div><p class="chart-caption">数据来源：MCP 股票数据服务</p></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartIncome'),{type:'bar',data:{labels:YEARS,datasets:[{label:'营收（亿元）',data:REVENUE,backgroundColor:'rgba(37,99,235,.75)',borderRadius:6,barPercentage:.6},{label:'净利润（亿元）',data:PROFIT,backgroundColor:'rgba(16,185,129,.75)',borderRadius:6,barPercentage:.6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{boxWidth:12,padding:16}}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'}},x:{grid:{display:false}}}}});
})();
</script>'''
        income_chart = income_chart.replace('YEARS', _iy).replace('REVENUE', _ir).replace('PROFIT', _ip)

    # Margin chart
    margin_chart = ''
    if has_margin and len(years) >= 3:
        _my = json.dumps(years)
        _md = json.dumps(margin_data)
        margin_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-percentage" style="color:#059669"></i> 毛利率趋势</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartMargin"></canvas></div></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartMargin'),{type:'line',data:{labels:YEARS,datasets:[{label:'毛利率（%）',data:MARGIN,borderColor:'#059669',backgroundColor:'rgba(5,150,105,.1)',fill:true,tension:.3,pointRadius:4,pointBackgroundColor:'#059669'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'},ticks:{callback:function(v){return v+'%'}}}},x:{grid:{display:false}}}}});
})();
</script>'''
        margin_chart = margin_chart.replace('YEARS', _my).replace('MARGIN', _md)

    # YoY growth chart
    yoy_chart = ''
    if has_yoy:
        _yoy_labels = json.dumps(yoy_labels)
        _yoy_data = json.dumps(yoy_data)
        yoy_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-arrow-trend-up" style="color:#059669"></i> 营收同比增长率</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartYoY"></canvas></div>
  <p class="chart-caption" style="margin-top:8px;font-size:.7rem;color:#94a3b8">
    <span style="display:inline-block;width:10px;height:10px;background:rgba(16,185,129,.75);border-radius:2px;margin-right:4px;vertical-align:middle"></span> 正增长
    <span style="display:inline-block;width:10px;height:10px;background:rgba(239,68,68,.75);border-radius:2px;margin-right:4px;margin-left:12px;vertical-align:middle"></span> 负增长
  </p>
  </div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartYoY'),{type:'bar',data:{labels:YOY_LABELS,datasets:[{label:'YoY %',data:YOY_DATA,backgroundColor:function(c){var v=c.raw;return v>=0?'rgba(16,185,129,.75)':'rgba(239,68,68,.75)'},borderRadius:6,barPercentage:.6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'rgba(0,0,0,.04)'},ticks:{callback:function(v){return v+'%'}}}},x:{grid:{display:false}}}}});
})();
</script>'''.replace('YOY_LABELS', _yoy_labels).replace('YOY_DATA', _yoy_data)

    exec_html = ''
    if exec_summary:
        exec_html = f'<div class="exec-box"><div class="label"><i class="fas fa-bolt" style="margin-right:4px"></i> 核心摘要</div>{parse_markdown(exec_summary)}</div>'

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{co}全面分析报告：{escape(subtitle)} — AI自习室</title>
  <meta name="description" content="深度分析{co}（{code}）：{industry}。AI 实时生成，覆盖财务、技术面、估值与风险分析。">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://aidev.fit/ai-analyst/{slug}.html">
  <link rel="alternate" hreflang="en" href="https://aidev.fit/en/ai-analyst/{slug}-en.html">
  <link rel="alternate" hreflang="zh-CN" href="https://aidev.fit/ai-analyst/{slug}.html">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
  body{{font-family:'Noto Sans SC','Inter',-apple-system,BlinkMacSystemFont,sans-serif;color:#1e293b;background:#f6f8fb;line-height:1.8;font-size:16px}}
  .report-wrap{{max-width:1100px;margin:0 auto;padding:20px;display:grid;grid-template-columns:220px 1fr;gap:32px}}
  @media(max-width:1023px){{.report-wrap{{grid-template-columns:1fr}}}}
  .toc-sidebar{{position:sticky;top:24px;height:fit-content;max-height:calc(100vh - 48px);overflow-y:auto}}
  .toc-sidebar::-webkit-scrollbar{{width:3px}}
  .toc-sidebar::-webkit-scrollbar-thumb{{background:#cbd5e1;border-radius:10px}}
  @media(max-width:1023px){{.toc-sidebar{{display:none}}}}
  .toc-title{{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#64748b;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}}
  .toc-list{{list-style:none;padding:0;margin:0}}
  .toc-list li{{margin-bottom:2px}}
  .toc-list a{{display:block;padding:6px 10px;border-radius:6px;font-size:.8rem;color:#64748b;text-decoration:none;transition:all .15s;line-height:1.3}}
  .toc-list a:hover{{background:#e8edf5;color:#2563eb}}
  .mobile-toc{{display:none}}
  @media(max-width:1023px){{.mobile-toc{{display:block;background:#fff;border-radius:12px;padding:16px 20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}}}
  .article-card{{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:48px 56px;margin-bottom:24px}}
  @media(max-width:768px){{.article-card{{padding:24px 20px;border-radius:0}}}}
  h1.report-title{{font-size:2.2rem;font-weight:900;color:#0f172a;line-height:1.2;text-align:center;letter-spacing:-.02em;margin-bottom:8px}}
  h2{{font-size:1.5rem!important;font-weight:700!important;color:#0f172a!important;margin-top:48px!important;margin-bottom:20px!important;padding-bottom:12px;border-bottom:3px solid #2563eb;display:flex;align-items:center;gap:10px}}
  h2 .section-num{{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:#2563eb;color:#fff;font-size:.85rem;font-weight:700;flex-shrink:0}}
  h3{{font-size:1.2rem!important;font-weight:600!important;color:#0f172a!important;margin-top:28px!important;margin-bottom:12px!important;padding-left:12px;border-left:3px solid #2563eb}}
  p{{font-size:1rem!important;margin-bottom:1.2em!important;color:#1e293b}}
  .badge-row{{display:flex;justify-content:center;gap:8px;margin-bottom:20px;flex-wrap:wrap}}
  .badge{{display:inline-block;padding:4px 14px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-radius:999px}}
  .report-meta{{text-align:center;margin:16px 0 32px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap}}
  .report-meta span{{font-size:.85rem;color:#64748b}}
  .report-meta strong{{color:#1e293b}}
  .stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:20px 0}}
  .stat-card{{background:#f8faff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 12px;text-align:center}}
  .stat-label{{font-size:.72rem;color:#64748b;margin-bottom:4px}}
  .stat-value{{font-size:1.1rem;font-weight:700;color:#1e293b}}
  .chart-card{{background:#fafcff;border:1px solid #e2e8f0;border-radius:12px;margin:24px 0;overflow:hidden}}
  .chart-header{{padding:14px 20px;border-bottom:1px solid #e2e8f0;font-size:.8rem;font-weight:600;color:#64748b;display:flex;align-items:center;gap:8px;background:#f8faff}}
  .chart-body{{padding:24px}}
  .chart-body .chart-container{{position:relative;height:280px;width:100%}}
  .chart-caption{{font-size:.75rem;color:#94a3b8;text-align:center;margin-top:12px}}
  .exec-box{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:12px;padding:24px;margin-bottom:28px}}
  .exec-box .label{{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#2563eb;margin-bottom:12px}}
  .exec-box p{{font-size:.9rem!important;color:#1e40af!important;margin-bottom:.8em!important;line-height:1.7}}
  .disclaimer-box{{margin-top:3rem;padding:1.5rem;background:#f9fafb;border-radius:10px;border:1px solid #e5e7eb;font-size:.8rem;color:#6b7280;line-height:1.6}}
  .disclaimer-box p{{font-size:.8rem!important;color:#6b7280!important;margin-bottom:0!important}}
  .btt-btn{{position:fixed;bottom:32px;right:32px;width:44px;height:44px;border-radius:50%;background:#2563eb;color:#fff;border:none;font-size:1.1rem;cursor:pointer;box-shadow:0 4px 12px rgba(37,99,235,.35);opacity:0;visibility:hidden;transition:all .2s;z-index:50;display:flex;align-items:center;justify-content:center}}
  .btt-btn.show{{opacity:1;visibility:visible}}
  @media(max-width:768px){{h1.report-title{{font-size:1.5rem!important}}h2{{font-size:1.2rem!important}}h3{{font-size:1.05rem!important}}p{{font-size:.9rem!important}}.article-card{{padding:20px 16px}}}}
  .indicator-signal{{display:inline-block;font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:99px;margin-top:4px}}
  .signal-buy{{background:#d1fae5;color:#065f46}}
  .signal-sell{{background:#fee2e2;color:#991b1b}}
  .signal-neutral{{background:#e5e7eb;color:#374151}}
  ol,ul{{margin:1em 0!important;padding-left:1.75rem!important}}
  ol li,ul li{{margin-bottom:.6em!important;line-height:1.7!important}}
  ol{{list-style:decimal!important}}
  ul{{list-style:disc!important}}
  table{{border-collapse:collapse;margin:1.5em 0!important;font-size:.9rem;width:100%}}
  th,td{{border:1px solid #e2e8f0;padding:8px 12px;text-align:left}}
  th{{background:#f8faff;font-weight:600;color:#475569}}
  tr:nth-child(even){{background:#fafcff}}
  </style>
</head>
<body class="bg-gray-50">
<div id="nav-placeholder"></div>
<div class="report-wrap">
  <nav class="toc-sidebar" aria-label="目录">
    <div class="toc-title">目录</div>
    <ul class="toc-list">
      {section_nav}
    </ul>
  </nav>
  <div class="report-content">
    <div class="mobile-toc">
      <select onchange="if(this.value)document.getElementById(this.value).scrollIntoView({{behavior:'smooth'}});this.selectedIndex=0;">
        <option value="">— 跳转到章节 —</option>
        {mobile_options}
      </select>
    </div>
    <article class="article-card">
      <header>
        <div class="badge-row">
          <span class="badge" style="background:#0f172a;color:#fff">Deep Research</span>
          <span class="badge" style="background:#1e3a5f;color:#fff">{co}</span>
          <span class="badge" style="background:#e8edf5;color:#475569">{code}</span>
        </div>
        <h1 class="report-title">{co}全面分析报告：{escape(subtitle)}</h1>
        <div class="report-meta">
          <span><strong>日期</strong> / <script>document.write(new Date().toLocaleDateString('zh-CN'))</script></span>
          <span><strong>行业</strong> / {escape(industry or '金融')}</span>
          <span><strong>来源</strong> / AI 生成</span>
        </div>
      </header>

      {exec_html}

      <div class="stat-grid">
        {stat_cards}
      </div>

      {section_html}

      {income_chart}
      {margin_chart}
      {yoy_chart}

      <div class="disclaimer-box">
        <p><strong>免责声明：</strong>本报告由AI自动生成，仅供参考和学习交流，不构成任何形式的投资建议。报告中的数据和分析基于公开信息和模型估算，可能存在偏差。股市有风险，投资需谨慎。作者和平台不对因使用本报告而产生的任何损失承担责任。</p>
      </div>
    </article>
    <div id="footer-placeholder"></div>
  </div>
</div>

<button class="btt-btn" id="bttBtn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="返回顶部"><i class="fas fa-arrow-up"></i></button>
<script>
window.addEventListener('scroll',function(){{document.getElementById('bttBtn').classList.toggle('show',window.scrollY>400)}});
</script>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<script src="/js/cookie-banner.js"></script>
</body>
</html>'''


def render_report_en(data):
    """Render EN report HTML — based on CN template but with English text."""
    co = escape(str(data.get('company', '') or ''))
    code = escape(str(data.get('code', '') or ''))
    slug = data.get('slug', 'report')
    industry = escape(str(data.get('industry_en', data.get('industry', '') or '')))
    price = data.get('latestPrice')
    pe = data.get('pe')
    pb = data.get('pb')
    high52 = data.get('high52')
    low52 = data.get('low52')
    subtitle = data.get('subtitle_en', data.get('subtitle', '')) or 'AI Deep Research'
    exec_summary = data.get('executive_summary_en', data.get('executive_summary', ''))
    sections = data.get('sections_en', data.get('sections', []))
    chart_data = data.get('chart_data', {})
    years = chart_data.get('years', [])
    rev_data = chart_data.get('revenue', [])
    profit_data = chart_data.get('netIncome', [])
    margin_data = chart_data.get('grossMargin', [])
    prices = chart_data.get('prices', [])

    has_margin = any(v is not None for v in (margin_data or []))

    # YoY growth data
    yoy_labels = years[1:] if len(years) > 1 else []
    yoy_data = []
    for i in range(len(rev_data) - 1):
        if rev_data[i] and rev_data[i] > 0:
            yoy_data.append(round((rev_data[i + 1] - rev_data[i]) / rev_data[i] * 100, 1))
        else:
            yoy_data.append(None)
    has_yoy = len(yoy_data) >= 2

    pct = None
    if price is not None and high52 is not None and low52 is not None and high52 > low52:
        pct = (price - low52) / (high52 - low52) * 100

    en_sections = [
        ('Company Overview', 'Business Overview', 'Financial Analysis', 'Technical Analysis',
         'Market Sentiment', 'Competitive Comparison', 'Valuation & Financial Health', 'Key Risks', 'Conclusion & Recommendations'),
    ][0]

    section_nav = ''
    mobile_options = ''
    section_html = ''

    for i in range(8):
        s_title = en_sections[i] if i < len(en_sections) else f'Section {i+1}'
        s_content = ''
        if i < len(sections):
            s_content = sections[i].get('content', '') if isinstance(sections[i], dict) else ''

        nav_icon = '<i class="fas fa-circle fa-fw" style="width:16px;color:#2563eb;font-size:.5rem;vertical-align:middle"></i>'
        section_nav += f'<li><a href="#s{i+1}">{nav_icon} {escape(s_title)}</a></li>\n'
        mobile_options += f'<option value="s{i+1}">{escape(s_title)}</option>\n'

        extra = ''
        if i == 2:
            extra = indicator_grid_html_en(price, pe, pb, pct)
            extra += price_chart_html(prices)

        sec_content = parse_markdown(s_content) if s_content else '<p>Insufficient data for this section.</p>'
        section_html += f'''
<h2 id="s{i+1}"><span class="section-num">{i+1}</span>{escape(s_title)}</h2>
{extra}
{sec_content}'''

    stat_cards = ''
    if price is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">Price</div><div class="stat-value">¥{price:.2f}</div></div>\n'
    if pe is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">P/E</div><div class="stat-value">{pe:.1f}x</div></div>\n'
    if pb is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">P/B</div><div class="stat-value">{pb:.2f}x</div></div>\n'
    if high52 is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">52W High</div><div class="stat-value">¥{high52:.2f}</div></div>\n'
    if low52 is not None:
        stat_cards += f'<div class="stat-card"><div class="stat-label">52W Low</div><div class="stat-value">¥{low52:.2f}</div></div>\n'

    income_chart = ''
    if len(years) >= 3:
        _iy = json.dumps(years)
        _ir = json.dumps(round_to_billion(rev_data))
        _ip = json.dumps(round_to_billion(profit_data))
        income_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-chart-bar" style="color:#2563eb"></i> Revenue & Net Income Trend</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartIncome"></canvas></div><p class="chart-caption">Source: MCP Stock Data</p></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartIncome'),{type:'bar',data:{labels:YEARS,datasets:[{label:'Revenue (CNY B)',data:REVENUE,backgroundColor:'rgba(37,99,235,.75)',borderRadius:6,barPercentage:.6},{label:'Net Income (CNY B)',data:PROFIT,backgroundColor:'rgba(16,185,129,.75)',borderRadius:6,barPercentage:.6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{boxWidth:12,padding:16}}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'}},x:{grid:{display:false}}}}});
})();
</script>'''
        income_chart = income_chart.replace('YEARS', _iy).replace('REVENUE', _ir).replace('PROFIT', _ip)

    margin_chart = ''
    if has_margin and len(years) >= 3:
        _my = json.dumps(years)
        _md = json.dumps(margin_data)
        margin_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-percentage" style="color:#059669"></i> Gross Margin Trend</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartMargin"></canvas></div></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartMargin'),{type:'line',data:{labels:YEARS,datasets:[{label:'Gross Margin (%)',data:MARGIN,borderColor:'#059669',backgroundColor:'rgba(5,150,105,.1)',fill:true,tension:.3,pointRadius:4,pointBackgroundColor:'#059669'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'},ticks:{callback:function(v){return v+'%'}}}},x:{grid:{display:false}}}}});
})();
</script>'''
        margin_chart = margin_chart.replace('YEARS', _my).replace('MARGIN', _md)

    # YoY growth chart
    yoy_chart = ''
    if has_yoy:
        _yoy_labels = json.dumps(yoy_labels)
        _yoy_data = json.dumps(yoy_data)
        yoy_chart = '''\
<div class="chart-card">
  <div class="chart-header"><i class="fas fa-arrow-trend-up" style="color:#059669"></i> Revenue YoY Growth</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartYoY"></canvas></div>
  <p class="chart-caption" style="margin-top:8px;font-size:.7rem;color:#94a3b8">
    <span style="display:inline-block;width:10px;height:10px;background:rgba(16,185,129,.75);border-radius:2px;margin-right:4px;vertical-align:middle"></span> Positive
    <span style="display:inline-block;width:10px;height:10px;background:rgba(239,68,68,.75);border-radius:2px;margin-right:4px;margin-left:12px;vertical-align:middle"></span> Negative
  </p>
  </div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
new Chart(document.getElementById('chartYoY'),{type:'bar',data:{labels:YOY_LABELS,datasets:[{label:'YoY %',data:YOY_DATA,backgroundColor:function(c){var v=c.raw;return v>=0?'rgba(16,185,129,.75)':'rgba(239,68,68,.75)'},borderRadius:6,barPercentage:.6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,grid:{color:'rgba(0,0,0,.04)'},ticks:{callback:function(v){return v+'%'}}}},x:{grid:{display:false}}}}});
})();
</script>'''.replace('YOY_LABELS', _yoy_labels).replace('YOY_DATA', _yoy_data)

    exec_html = ''
    if exec_summary:
        exec_html = f'<div class="exec-box"><div class="label"><i class="fas fa-bolt" style="margin-right:4px"></i> Executive Summary</div>{parse_markdown(exec_summary)}</div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{co} Comprehensive Investment Analysis (2026) — AI Study Room</title>
  <meta name="description" content="In-depth analysis of {co} ({code}): {industry}. AI-generated comprehensive investment research covering financials, technicals, valuation and risks.">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://aidev.fit/en/ai-analyst/{slug}-en.html">
  <link rel="alternate" hreflang="en" href="https://aidev.fit/en/ai-analyst/{slug}-en.html">
  <link rel="alternate" hreflang="zh-CN" href="https://aidev.fit/ai-analyst/{slug}.html">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
  [same styles as CN template for consistency]{{
  body{{font-family:'Inter','Noto Sans SC',-apple-system,BlinkMacSystemFont,sans-serif;color:#1e293b;background:#f6f8fb;line-height:1.8;font-size:16px}}
  .report-wrap{{max-width:1100px;margin:0 auto;padding:20px;display:grid;grid-template-columns:220px 1fr;gap:32px}}
  @media(max-width:1023px){{.report-wrap{{grid-template-columns:1fr}}}}
  .toc-sidebar{{position:sticky;top:24px;height:fit-content;max-height:calc(100vh - 48px);overflow-y:auto}}
  .toc-sidebar::-webkit-scrollbar{{width:3px}}
  .toc-sidebar::-webkit-scrollbar-thumb{{background:#cbd5e1;border-radius:10px}}
  @media(max-width:1023px){{.toc-sidebar{{display:none}}}}
  .toc-title{{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#64748b;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}}
  .toc-list{{list-style:none;padding:0;margin:0}}
  .toc-list li{{margin-bottom:2px}}
  .toc-list a{{display:block;padding:6px 10px;border-radius:6px;font-size:.8rem;color:#64748b;text-decoration:none;transition:all .15s;line-height:1.3}}
  .toc-list a:hover{{background:#e8edf5;color:#2563eb}}
  .mobile-toc{{display:none}}
  @media(max-width:1023px){{.mobile-toc{{display:block;background:#fff;border-radius:12px;padding:16px 20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}}}
  .article-card{{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:48px 56px;margin-bottom:24px}}
  @media(max-width:768px){{.article-card{{padding:24px 20px;border-radius:0}}}}
  h1.report-title{{font-size:2.2rem;font-weight:900;color:#0f172a;line-height:1.2;text-align:center;letter-spacing:-.02em;margin-bottom:8px}}
  h2{{font-size:1.5rem!important;font-weight:700!important;color:#0f172a!important;margin-top:48px!important;margin-bottom:20px!important;padding-bottom:12px;border-bottom:3px solid #2563eb;display:flex;align-items:center;gap:10px}}
  h2 .section-num{{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:#2563eb;color:#fff;font-size:.85rem;font-weight:700;flex-shrink:0}}
  h3{{font-size:1.2rem!important;font-weight:600!important;color:#0f172a!important;margin-top:28px!important;margin-bottom:12px!important;padding-left:12px;border-left:3px solid #2563eb}}
  p{{font-size:1rem!important;margin-bottom:1.2em!important;color:#1e293b}}
  .exec-box{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:12px;padding:24px;margin-bottom:28px}}
  .exec-box .label{{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#2563eb;margin-bottom:12px}}
  .exec-box p{{font-size:.9rem!important;color:#1e40af!important;margin-bottom:.8em!important;line-height:1.7}}
  .stat-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:20px 0}}
  .stat-card{{background:#f8faff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 12px;text-align:center}}
  .stat-label{{font-size:.72rem;color:#64748b;margin-bottom:4px}}
  .stat-value{{font-size:1.1rem;font-weight:700;color:#1e293b}}
  .chart-card{{background:#fafcff;border:1px solid #e2e8f0;border-radius:12px;margin:24px 0;overflow:hidden}}
  .chart-header{{padding:14px 20px;border-bottom:1px solid #e2e8f0;font-size:.8rem;font-weight:600;color:#64748b;display:flex;align-items:center;gap:8px;background:#f8faff}}
  .chart-body{{padding:24px}}
  .chart-body .chart-container{{position:relative;height:280px;width:100%}}
  .chart-caption{{font-size:.75rem;color:#94a3b8;text-align:center;margin-top:12px}}
  .indicator-signal{{display:inline-block;font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:99px;margin-top:4px}}
  .signal-buy{{background:#d1fae5;color:#065f46}}
  .signal-sell{{background:#fee2e2;color:#991b1b}}
  .signal-neutral{{background:#e5e7eb;color:#374151}}
  .disclaimer-box{{margin-top:3rem;padding:1.5rem;background:#f9fafb;border-radius:10px;border:1px solid #e5e7eb;font-size:.8rem;color:#6b7280;line-height:1.6}}
  .disclaimer-box p{{font-size:.8rem!important;color:#6b7280!important;margin-bottom:0!important}}
  .badge-row{{display:flex;justify-content:center;gap:8px;margin-bottom:20px;flex-wrap:wrap}}
  .badge{{display:inline-block;padding:4px 14px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-radius:999px}}
  .report-meta{{text-align:center;margin:16px 0 32px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap}}
  .report-meta span{{font-size:.85rem;color:#64748b}}
  .report-meta strong{{color:#1e293b}}
  ol,ul{{margin:1em 0!important;padding-left:1.75rem!important}}
  ol li,ul li{{margin-bottom:.6em!important;line-height:1.7!important}}
  ol{{list-style:decimal!important}}
  ul{{list-style:disc!important}}
  table{{border-collapse:collapse;margin:1.5em 0!important;font-size:.9rem;width:100%}}
  th,td{{border:1px solid #e2e8f0;padding:8px 12px;text-align:left}}
  th{{background:#f8faff;font-weight:600;color:#475569}}
  tr:nth-child(even){{background:#fafcff}}
  </style>
</head>
<body class="bg-gray-50">
<div id="nav-placeholder"></div>
<div class="report-wrap">
  <nav class="toc-sidebar" aria-label="Table of Contents">
    <div class="toc-title">Contents</div>
    <ul class="toc-list">
      {section_nav}
    </ul>
  </nav>
  <div class="report-content">
    <div class="mobile-toc">
      <select onchange="if(this.value)document.getElementById(this.value).scrollIntoView({{behavior:'smooth'}});this.selectedIndex=0;">
        <option value="">— Jump to section —</option>
        {mobile_options}
      </select>
    </div>
    <article class="article-card">
      <header>
        <div class="badge-row">
          <span class="badge" style="background:#0f172a;color:#fff">Deep Research</span>
          <span class="badge" style="background:#1e3a5f;color:#fff">{co}</span>
          <span class="badge" style="background:#e8edf5;color:#475569">{code}</span>
        </div>
        <h1 class="report-title">{co} Comprehensive Investment Analysis (2026)</h1>
        <div class="report-meta">
          <span><strong>Date</strong> / <script>document.write(new Date().toLocaleDateString('en-US'))</script></span>
          <span><strong>Sector</strong> / {escape(industry or 'Finance')}</span>
          <span><strong>Source</strong> / AI Generated</span>
        </div>
      </header>

      {exec_html}

      <div class="stat-grid">
        {stat_cards}
      </div>

      {section_html}

      {income_chart}
      {margin_chart}
      {yoy_chart}

      <div class="disclaimer-box">
        <p><strong>Disclaimer:</strong> This report is AI-generated for informational purposes only and does not constitute investment advice. Analyses are based on public data and model estimates, which may contain errors. Investing involves risk.</p>
      </div>
    </article>
    <div id="footer-placeholder"></div>
  </div>
</div>

<button class="btt-btn" id="bttBtn" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="Back to top"><i class="fas fa-arrow-up"></i></button>
<script>
window.addEventListener('scroll',function(){{document.getElementById('bttBtn').classList.toggle('show',window.scrollY>400)}});
</script>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<script src="/js/cookie-banner.js"></script>
</body>
</html>'''


def indicator_grid_html(price, pe, pb, pct):
    """CN indicator grid."""
    d3pe = f'{pe:.1f}x' if pe is not None else '—'
    d3pb = f'{pb:.2f}x' if pb is not None else '—'
    d3pos = f'{pct:.0f}%' if pct is not None else '—'
    d3pct = pct if pct is not None else 50
    d3price = f'{price:.2f}' if price is not None else '—'

    pe_signal = '偏高' if (pe or 0) > 50 else ('偏低' if (pe or 100) < 15 else '适中')
    pb_signal = '偏高' if (pb or 0) > 5 else ('偏低' if (pb or 100) < 1 else '适中')
    pos_signal = 'signal-sell' if d3pct > 80 else ('signal-buy' if d3pct < 20 else 'signal-neutral')
    pos_label = '高位' if d3pct > 80 else ('低位' if d3pct < 20 else '中位')
    pos2_label = '关注回调' if d3pct > 80 else ('关注反弹' if d3pct < 30 else '区间震荡')
    pos2_signal = 'signal-sell' if d3pct > 80 else ('signal-buy' if d3pct < 30 else 'signal-neutral')

    return f'''<div class="chart-card">
  <div class="chart-header"><i class="fas fa-gauge-high" style="color:#2563eb"></i> 核心指标</div>
  <div class="chart-body">
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-label">PE</div><div class="stat-value">{d3pe}</div><span class="indicator-signal signal-neutral">{pe_signal}</span></div>
      <div class="stat-card"><div class="stat-label">PB</div><div class="stat-value">{d3pb}</div><span class="indicator-signal signal-neutral">{pb_signal}</span></div>
      <div class="stat-card"><div class="stat-label">52周位置</div><div class="stat-value">{d3pos}</div><span class="indicator-signal {pos_signal}">{pos_label}</span></div>
      <div class="stat-card"><div class="stat-label">当前价</div><div class="stat-value">¥{d3price}</div><span class="indicator-signal {pos2_signal}">{pos2_label}</span></div>
    </div>
  </div>
</div>'''


def indicator_grid_html_en(price, pe, pb, pct):
    """EN indicator grid."""
    d3pe = f'{pe:.1f}x' if pe is not None else '—'
    d3pb = f'{pb:.2f}x' if pb is not None else '—'
    d3pos = f'{pct:.0f}%' if pct is not None else '—'
    d3pct = pct if pct is not None else 50
    d3price = f'{price:.2f}' if price is not None else '—'

    pe_signal = 'Premium' if (pe or 0) > 50 else ('Discount' if (pe or 100) < 15 else 'Fair')
    pb_signal = 'Premium' if (pb or 0) > 5 else ('Discount' if (pb or 100) < 1 else 'Fair')
    pos_signal = 'signal-sell' if d3pct > 80 else ('signal-buy' if d3pct < 20 else 'signal-neutral')
    pos_label = 'High' if d3pct > 80 else ('Low' if d3pct < 20 else 'Mid')
    pos2_label = 'Caution' if d3pct > 80 else ('Oversold' if d3pct < 30 else 'Range')
    pos2_signal = 'signal-sell' if d3pct > 80 else ('signal-buy' if d3pct < 30 else 'signal-neutral')

    return f'''<div class="chart-card">
  <div class="chart-header"><i class="fas fa-gauge-high" style="color:#2563eb"></i> Key Indicators</div>
  <div class="chart-body">
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-label">P/E</div><div class="stat-value">{d3pe}</div><span class="indicator-signal signal-neutral">{pe_signal}</span></div>
      <div class="stat-card"><div class="stat-label">P/B</div><div class="stat-value">{d3pb}</div><span class="indicator-signal signal-neutral">{pb_signal}</span></div>
      <div class="stat-card"><div class="stat-label">52W Pos.</div><div class="stat-value">{d3pos}</div><span class="indicator-signal {pos_signal}">{pos_label}</span></div>
      <div class="stat-card"><div class="stat-label">Price</div><div class="stat-value">¥{d3price}</div><span class="indicator-signal {pos2_signal}">{pos2_label}</span></div>
    </div>
  </div>
</div>'''


def price_chart_html(prices):
    """Price chart HTML — same for CN and EN."""
    if not prices or len(prices) < 5:
        return ''
    dates = json.dumps([p.get('date', '') for p in prices])
    closes = json.dumps([p.get('close', 0) for p in prices])
    return '''<div class="chart-card">
  <div class="chart-header"><i class="fas fa-chart-line" style="color:#2563eb"></i> Price Trend</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartPrice"></canvas></div></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
var _d=DATES;
var _c=CLOSES;
new Chart(document.getElementById('chartPrice'),{type:'line',data:{labels:_d,datasets:[{label:'Close (CNY)',data:_c,borderColor:'#2563eb',backgroundColor:'rgba(37,99,235,.08)',fill:true,tension:.3,pointRadius:2,pointHoverRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'}},x:{grid:{display:false},ticks:{maxTicksLimit:8}}}}});
})();
</script>'''.replace('DATES', dates).replace('CLOSES', closes)


# ═══════════════════════════════ Markdown Parser ═══════════════════════════════

def parse_markdown(text):
    """Parse basic markdown → HTML (ported from renderer.js)."""
    if not text:
        return ''
    lines = text.split('\n')
    out = []
    in_ul = False
    in_ol = False
    in_table = False

    def close_lists():
        nonlocal in_ul, in_ol, in_table
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False
        if in_table:
            out.append('</tbody></table>')
            in_table = False

    for i, raw in enumerate(lines):
        trimmed = raw.strip()

        if not trimmed:
            close_lists()
            continue

        # ### Heading
        if trimmed.startswith('### '):
            close_lists()
            out.append(f'<h3>{inline_md(escape(trimmed[4:]))}</h3>')
            continue

        # Table separator row |---|---| — skip silently
        if re.match(r'^\|[\s\-:|]+\|$', trimmed):
            continue

        # Table row |...|
        if trimmed.startswith('|') and trimmed.endswith('|'):
            cells = [inline_md(escape(c.strip())) for c in trimmed.split('|') if c.strip()]
            if not cells:
                continue
            next_is_header = (i + 1 < len(lines)) and bool(re.match(r'^\|[\s\-:|]+\|$', lines[i + 1].strip()))
            if next_is_header:
                if in_table:
                    out.append('</tbody></table>')
                out.append('<table><thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead><tbody>')
                in_table = True
            elif in_table:
                out.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
            else:
                out.append('<table><tbody><tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
                in_table = True
            continue

        # Unordered list
        if re.match(r'^[-*]\s', trimmed):
            if in_ol:
                out.append('</ol>')
                in_ol = False
            if in_table:
                out.append('</tbody></table>')
                in_table = False
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'<li>{inline_md(escape(re.sub(r"^[-*]\s+", "", trimmed)))}</li>')
            continue

        # Ordered list
        if re.match(r'^\d+[.)]\s', trimmed):
            if in_ul:
                out.append('</ul>')
                in_ul = False
            if in_table:
                out.append('</tbody></table>')
                in_table = False
            if not in_ol:
                out.append('<ol>')
                in_ol = True
            out.append(f'<li>{inline_md(escape(re.sub(r"^\d+[.)]\s+", "", trimmed)))}</li>')
            continue

        # Paragraph
        close_lists()
        out.append(f'<p>{inline_md(escape(trimmed))}</p>')

    close_lists()
    return '\n'.join(out)


def inline_md(text):
    """**bold** conversion."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


# ═══════════════════════════════ Helpers ═══════════════════════════════

def fmt_num(v):
    """Format number to 万元/亿元."""
    if v is None:
        return None
    try:
        n = float(v)
    except (ValueError, TypeError):
        return str(v)
    if abs(n) >= 1e8:
        return f'{n / 1e8:.2f}亿'
    if abs(n) >= 1e4:
        return f'{n / 1e4:.2f}万'
    return f'{n:.2f}'


def round_to_billion(arr):
    """Convert yuan amounts to 亿元 for charts."""
    return [round(v / 1e8, 2) if v is not None else None for v in arr]


def make_slug(name, code):
    """Generate URL slug."""
    return f'{code}-{datetime.now(timezone.utc).strftime("%Y")}'


def load_queue():
    """Load stock queue (list of companies)."""
    if not QUEUE_FILE.exists():
        return []
    with open(QUEUE_FILE) as f:
        return json.load(f)


def load_progress():
    """Load generation progress."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {'generated': [], 'lastRun': None}


def save_progress(progress):
    """Save generation progress."""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def register_article_cn(company_name, stock_code, slug, title):
    """Register CN article in articles.json."""
    with open(ARTICLES_CN) as f:
        articles = json.load(f)

    for board in articles['boards']:
        if board['id'] == 'ai-analyst':
            posts = board['posts']
            if any(p['slug'] == slug for p in posts):
                print(f'  Already registered in CN, skipping')
                return True
            next_id = max(p['id'] for p in posts) + 1
            posts.append({
                'id': next_id,
                'slug': slug,
                'title': title,
                'description': f'深度分析{company_name}（{stock_code}）：AI 深度研究报告，覆盖财务、技术面、竞品、估值与风险分析。',
                'date': TODAY,
                'lastActive': TODAY,
                'tags': [company_name, '投资分析', '深度研究'],
                'replies': 0,
                'views': 0,
            })
            print(f'  Registered CN: id={next_id}')
            break

    with open(ARTICLES_CN, 'w') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    return True


def register_article_en(company_name, stock_code, slug, title):
    """Register EN article in en/articles.json."""
    with open(ARTICLES_EN) as f:
        articles = json.load(f)

    en_slug = f'{slug}-en'
    for board in articles['boards']:
        if board['id'] == 'ai-analyst':
            posts = board['posts']
            if any(p['slug'] == en_slug for p in posts):
                print(f'  Already registered in EN, skipping')
                return True
            posts.append({
                'id': 0,
                'slug': en_slug,
                'title': title,
                'description': f'In-depth analysis of {company_name} ({stock_code}): AI-driven comprehensive research covering financials, technicals, competitive analysis, valuation, and risks.',
                'date': TODAY,
                'lastActive': TODAY,
                'tags': ['AI Analyst', 'Investment Analysis', 'Deep Research'],
                'replies': 0,
                'views': 0,
                'board': 'ai-analyst',
            })
            print(f'  Registered EN: slug={en_slug}')
            break

    with open(ARTICLES_EN, 'w') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    return True


def update_index_html_cn(slug, title):
    """Append new article to CN index.html JSON-LD + noscript list."""
    with open(INDEX_CN) as f:
        content = f.read()

    filename = f'{slug}.html'
    url = f'https://aidev.fit/ai-analyst/{filename}'

    # Update description count
    # Count current posts in articles.json
    with open(ARTICLES_CN) as f:
        articles = json.load(f)
    count = 0
    for b in articles['boards']:
        if b['id'] == 'ai-analyst':
            count = len(b['posts'])
            break

    content = re.sub(r'（\d+ 篇文章）', f'（{count} 篇文章）', content)

    # JSON-LD — add to CollectionPage
    ld_match = re.search(
        r'(<script type="application/ld\+json">\s*)(\{.*?"@type"\s*:\s*"CollectionPage".*?itemListElement.*?\}\s*\})\s*(</script>)',
        content, re.DOTALL,
    )
    if ld_match:
        ld_json = json.loads(ld_match.group(2))
        items = ld_json.get('mainEntity', {}).get('itemListElement', [])
        if not any(item.get('url') == url for item in items):
            items.append({'@type': 'ListItem', 'position': len(items) + 1, 'url': url})
            ld_json['numberOfItems'] = len(items)
            ld_json['mainEntity']['itemListElement'] = items
            new_ld = json.dumps(ld_json, ensure_ascii=False)
            content = content[:ld_match.start(2)] + new_ld + content[ld_match.end(2):]

    # Noscript list — add <li>
    li_tag = f'<li><a href="/ai-analyst/{filename}">{escape(title)}</a> <small>{TODAY}</small></li>'
    if f'href="/ai-analyst/{filename}"' not in content:
        content = content.replace(
            '</ul></noscript></div>',
            f'{li_tag}\n</ul></noscript></div>',
        )

    with open(INDEX_CN, 'w') as f:
        f.write(content)
    print('  CN index.html updated')


def update_index_html_en(slug, title):
    """Append new article to EN index.html JSON-LD + noscript list."""
    if not INDEX_EN.exists():
        print('  EN index.html not found, skipping')
        return

    with open(INDEX_EN) as f:
        content = f.read()

    en_slug = f'{slug}-en'
    filename = f'{en_slug}.html'

    # JSON-LD
    ld_match = re.search(
        r'(<script type="application/ld\+json">\s*)(\{.*?"@type"\s*:\s*"CollectionPage".*?itemListElement.*?\}\s*\})\s*(</script>)',
        content, re.DOTALL,
    )
    if ld_match:
        ld_json = json.loads(ld_match.group(2))
        items = ld_json.get('mainEntity', {}).get('itemListElement', [])
        url = f'https://aidev.fit/en/ai-analyst/{filename}'
        if not any(item.get('url') == url for item in items):
            items.append({'@type': 'ListItem', 'position': len(items) + 1, 'url': url})
            ld_json['numberOfItems'] = len(items)
            ld_json['mainEntity']['itemListElement'] = items
            new_ld = json.dumps(ld_json, ensure_ascii=False)
            content = content[:ld_match.start(2)] + new_ld + content[ld_match.end(2):]

    # Noscript
    li_tag = f'<li><a href="/en/ai-analyst/{filename}">{escape(title)}</a> <small>{TODAY}</small></li>'
    if f'href="/en/ai-analyst/{filename}"' not in content:
        content = content.replace(
            '</ul></noscript></div>',
            f'{li_tag}\n</ul></noscript></div>',
        )

    with open(INDEX_EN, 'w') as f:
        f.write(content)
    print('  EN index.html updated')


# ═══════════════════════════════ Company Generation ═══════════════════════════════

def generate_one(name, code, sector):
    """Generate report for one company: fetch data → LLM → render → save."""
    print(f'\n── Generating report for {name} ({code}) ──')

    # 1. Basic info
    basic_rows = mcp_extract_rows(get_basic_info(code))
    basic = basic_rows[0] if basic_rows else {}
    print(f'  Industry: {basic.get("industry", "N/A")}')

    # 2. Financial data
    income = get_income(code)
    bs = get_balance_sheet(code)
    cf = get_cash_flow(code)
    quotes = get_quotes(code)

    income_rows = mcp_extract_rows(income)
    bs_rows = mcp_extract_rows(bs)
    cf_rows = mcp_extract_rows(cf)
    quote_rows = mcp_extract_rows(quotes)

    latest_income = income_rows[0] if income_rows else {}
    latest_bs = bs_rows[0] if bs_rows else {}

    # 3. Price data
    prices = [
        {'date': q.get('tradeDate') or q.get('date', ''), 'close': float(q.get('closePrice') or q.get('close', 0))}
        for q in quote_rows if float(q.get('closePrice', 0) or q.get('close', 0)) > 0
    ]
    prices.reverse()
    high52 = max(p['close'] for p in prices) if prices else None
    low52 = min(p['close'] for p in prices) if prices else None
    latest_price = prices[-1]['close'] if prices else None

    # Debug: print MCP income data structure
    if income_rows:
        keys = list(income_rows[0].keys())[:30]
        yr_val = income_rows[0].get('endDate', 'N/A')
        rev_val = income_rows[0].get('revenue', income_rows[0].get('totalOperatingRevenue', 'N/A'))
        np_val = income_rows[0].get('netProfit', income_rows[0].get('netIncome', 'N/A'))
        rd_val = income_rows[0].get('reportPeriodEnd', 'N/A')
        gp_val = income_rows[0].get('grossProfitMargin', 'N/A')
        print(f'  Income rows: {len(income_rows)}, keys: {keys}')
        print(f'  Sample: yr={yr_val}, rd={rd_val}, rev={rev_val}, np={np_val}, gp={gp_val}')

    # 4. Chart data (multi-year)
    years = []
    rev_data = []
    profit_data = []
    margin_data = []

    for r in reversed(income_rows):
        yr = (r.get('endDate') or r.get('reportDate') or r.get('reportPeriodEnd', ''))[:4]
        if yr and (not years or yr != years[-1]):
            years.append(yr)
            rev = float(r.get('totalOperatingRevenue') or r.get('revenue') or r.get('operatingRevenue', 0) or 0)
            profit = float(r.get('netProfit') or r.get('netIncome') or 0)
            rev_data.append(rev)
            profit_data.append(profit)

            gp = r.get('grossProfitMargin')
            if gp is not None:
                margin_data.append(float(gp))
            else:
                gp_rev = rev
                gp_amt = float(r.get('grossProfit', 0) or 0)
                if gp_rev > 0 and gp_amt > 0:
                    margin_data.append(round(gp_amt / gp_rev * 100, 2))
                else:
                    margin_data.append(None)

    # Only take unique years
    seen_years = set()
    dedup = []
    for i, yr in enumerate(years):
        if yr not in seen_years:
            seen_years.add(yr)
            dedup.append(i)
    years = [years[i] for i in dedup]
    rev_data = [rev_data[i] for i in dedup]
    profit_data = [profit_data[i] for i in dedup]
    margin_data = [margin_data[i] for i in dedup]

    # 5. Build prompt and call DeepSeek
    prompt = build_prompt({
        'name': name, 'code': code,
        'industry': basic.get('industry', ''),
        'marketCap': fmt_num(basic.get('totalMarketCap')),
        'price': latest_price, 'high52': high52, 'low52': low52,
        'pe': basic.get('peRatio') or basic.get('pe'),
        'pb': basic.get('pbRatio') or basic.get('pb'),
        'years': years, 'rev_data': rev_data, 'profit_data': profit_data,
        'margin_data': margin_data,
        'income_rows': income_rows,
    })

    print('  Calling Qwen...', end=' ', flush=True)
    report = deepseek_generate(prompt)
    print('Done')

    subtitle = report.get('subtitle', 'AI 深度研究')
    exec_summary = report.get('executive_summary', '')
    sections = report.get('sections', [])

    # Translate EN — for now use same content as CN (marked for future bilingual LLM generation)
    # LLM generates in Chinese; we use the same content for EN version
    # In a future upgrade, the LLM can generate both in one call
    subtitle_en = f'{name} ({code}) — AI Deep Research'
    exec_summary_en = exec_summary  # Will improve with dedicated EN prompt later
    sections_en = sections  # Same content, rendered in EN template

    # 6. Save CN HTML
    slug = make_slug(name, code)
    cn_data = {
        'company': name, 'code': code,
        'industry': basic.get('industry', ''),
        'latestPrice': latest_price, 'high52': high52, 'low52': low52,
        'pe': basic.get('peRatio') or basic.get('pe'),
        'pb': basic.get('pbRatio') or basic.get('pb'),
        'slug': slug, 'subtitle': subtitle,
        'executive_summary': exec_summary,
        'sections': sections,
        'chart_data': {
            'years': years, 'revenue': rev_data,
            'netIncome': profit_data, 'grossMargin': margin_data,
            'prices': prices,
        },
    }

    cn_html = render_report_cn(cn_data)
    cn_file = REPORTS_CN_DIR / f'{slug}.html'
    cn_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cn_file, 'w') as f:
        f.write(cn_html)
    print(f'  Saved CN: ai-analyst/{slug}.html ({len(cn_html)} bytes)')

    # 7. Save EN HTML
    en_data = cn_data.copy()
    en_data['slug'] = f'{slug}-en'
    en_data['subtitle'] = subtitle_en
    en_data['executive_summary'] = exec_summary_en
    en_data['sections'] = sections_en

    en_html = render_report_en(en_data)
    en_file = REPORTS_EN_DIR / f'{slug}-en.html'
    en_file.parent.mkdir(parents=True, exist_ok=True)
    with open(en_file, 'w') as f:
        f.write(en_html)
    print(f'  Saved EN: en/ai-analyst/{slug}-en.html ({len(en_html)} bytes)')

    # 8. Register in articles.json
    cn_title = f'{name}全面分析报告：{subtitle}'
    en_title = f'{name} Comprehensive Investment Analysis (2026)'

    register_article_cn(name, code, slug, cn_title)
    register_article_en(name, code, slug, en_title)

    # 9. Update index.html
    update_index_html_cn(slug, cn_title)
    update_index_html_en(slug, en_title)

    return {
        'name': name, 'code': code, 'slug': slug,
        'cn_file': f'ai-analyst/{slug}.html',
        'en_file': f'en/ai-analyst/{slug}-en.html',
        'cn_title': cn_title,
        'en_title': en_title,
    }


# ═══════════════════════════════ Main ═══════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Generate AI analyst reports from stock queue')
    parser.add_argument('--list', action='store_true', help='Show queue status')
    parser.add_argument('--reset', action='store_true', help='Reset progress (re-generate all)')
    parser.add_argument('--company', type=str, help='Generate report for a single company by name')
    parser.add_argument('--code', type=str, help='Stock code (used with --company)')
    args = parser.parse_args()

    if not MCP_URL or not MCP_TOKEN or not DEEPSEEK_KEY:
        print('Error: Set MCP_URL, MCP_TOKEN, and DEEPSEEK_KEY environment variables')
        print('')
        print('  export MCP_URL="https://dashscope.aliyuncs.com/api/v1/mcps/..."')
        print('  export MCP_TOKEN="Bearer sk-..."')
        print('  export DEEPSEEK_KEY="sk-..."')
        sys.exit(1)

    # --company mode: generate for one specific company
    if args.company:
        name = args.company.strip()
        code = args.code.strip() if args.code else ''
        if not code:
            print(f'Searching for {name}...')
            sr = search_stock(name)
            rows = mcp_extract_rows(sr)
            if not rows:
                print(f'Error: Could not find stock code for "{name}"')
                sys.exit(1)
            code = str(rows[0].get('code', rows[0].get('stockCode', ''))).replace('.SZ', '').replace('.SH', '')
            name = rows[0].get('shortName') or rows[0].get('stockName') or rows[0].get('name') or name
            print(f'  Found: {name} ({code})')

        sector = ''
        try:
            basic = get_basic_info(code)
            sector = basic.get('industry', '')
        except Exception:
            pass

        result = generate_one(name, code, sector)
        print(f'\n✅ Generated: {result["cn_file"]}')
        if not args.code:
            print('  Use --code to skip search next time')
        return

    # --list mode
    if args.list:
        queue = load_queue()
        progress = load_progress()
        total = len(queue)
        done = len(progress['generated'])
        remaining = total - done
        print(f'Queue: {total} companies')
        print(f'Generated: {done}')
        print(f'Remaining: {remaining}')
        print(f'Last run: {progress.get("lastRun", "never")}')
        if queue:
            print(f'\nFirst 10 remaining:')
            for item in queue:
                slug = make_slug(item['name'], item['code'])
                if slug not in progress['generated']:
                    print(f'  - {item["name"]} ({item["code"]}) [{item.get("sector", "N/A")}]')
                    remaining -= 1
                    if remaining <= 0:
                        break
        return

    # --reset mode
    if args.reset:
        progress = {'generated': [], 'lastRun': None}
        save_progress(progress)
        print('Progress reset. All companies can be re-generated.')
        return

    # Default: generate next BATCH_SIZE companies
    queue = load_queue()
    if not queue:
        print('Error: No stock queue found. Create data/stock-queue.json first.')
        print('Example format:')
        print('  [')
        print('    {"name": "中芯国际", "code": "688981", "sector": "半导体"},')
        print('    {"name": "北方华创", "code": "002371", "sector": "半导体"},')
        print('    ...')
        print('  ]')
        sys.exit(1)

    progress = load_progress()
    pending = []
    for item in queue:
        slug = make_slug(item['name'], item['code'])
        if slug not in progress['generated']:
            pending.append(item)
        if len(pending) >= BATCH_SIZE:
            break

    if not pending:
        print('All companies in queue have been generated! Use --reset to regenerate.')
        return

    print(f'Generating {len(pending)} reports...')
    results = []
    for item in pending:
        try:
            result = generate_one(item['name'], item['code'], item.get('sector', ''))
            results.append(result)

            # Mark as generated
            slug = make_slug(item['name'], item['code'])
            progress['generated'].append(slug)
            progress['lastRun'] = datetime.now(timezone.utc).isoformat()
            save_progress(progress)

            # Rate limit: 30s between companies
            if len(pending) > 1:
                print('  Waiting 30s for rate limiting...')
                time.sleep(30)
        except Exception as e:
            print(f'  ❌ Error generating {item["name"]}: {e}')
            import traceback
            traceback.print_exc()

    # Summary
    print('\n' + '=' * 60)
    print(f'Generated {len(results)} reports:')
    for r in results:
        print(f'  ✅ {r["name"]} ({r["code"]})')
        print(f'     CN: {r["cn_file"]}')
        print(f'     EN: {r["en_file"]}')
    print(f'\nCommit and push to deploy.')
    print(f'Queue remaining: {len(queue) - len(progress["generated"])}')


if __name__ == '__main__':
    main()

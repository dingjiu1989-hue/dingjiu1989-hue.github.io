import { searchStock, getBasicInfo, getIncome, getBalanceSheet, getCashFlow, getAdjustedQuotes } from './mcp.js';
import { deepseekReport } from './deepseek.js';
import { validateMCPData, validateReport } from './validator.js';
import { renderReportHTML } from './renderer.js';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}

function html(body, status = 200) {
  return new Response(body, {
    status,
    headers: { ...CORS, 'Content-Type': 'text/html;charset=utf-8' },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });

    const url = new URL(request.url);
    const path = url.pathname.replace(/\/$/, '') || '';
    const kv = env.AI_ANALYST_REQUESTS;

    // ── GET /report/<slug> — serve generated report HTML ──
    if (request.method === 'GET' && path.startsWith('/report/')) {
      const slug = path.replace('/report/', '');
      if (!slug) return json({ error: 'missing slug' }, 400);
      const content = await kv.get(`report:${slug}`, { type: 'text' });
      if (!content) return html('<h1>404 - 报告未找到</h1>', 404);
      return html(content);
    }

    // ── POST — generate report ──
    if (request.method !== 'POST') return json({ error: '仅支持 POST' }, 405);

    let company;
    try {
      const body = await request.json();
      company = body.company;
    } catch {
      return json({ error: '无效的请求体' }, 400);
    }

    if (!company || typeof company !== 'string' || company.trim().length === 0) {
      return json({ error: '请输入公司名称' }, 400);
    }

    const name = company.trim();
    const mcpUrl = env.MCP_URL;
    const mcpToken = env.MCP_TOKEN;
    const dsKey = env.DEEPSEEK_KEY;

    if (!mcpUrl || !mcpToken) return json({ error: 'MCP 未配置' }, 500);
    if (!dsKey) return json({ error: 'DeepSeek API Key 未配置' }, 500);

    try {
      // Step 1: Search stock code
      const searchResult = await searchStock(mcpUrl, mcpToken, name);
      const stocks = extractRows(searchResult);
      if (!stocks.length) {
        return json({ error: `未找到「${name}」的股票代码，可能暂未覆盖` }, 404);
      }
      const stock = stocks[0];
      const code = String(stock.code || stock.stockCode || '').replace(/\.SZ|\.SH/gi, '');
      const stockName = stock.shortName || stock.stockName || stock.name || name;

      // Step 2: Get financial data
      const [basicInfo, income, balanceSheet, cashFlow, quotes] = await Promise.all([
        getBasicInfo(mcpUrl, mcpToken, code).catch(() => ({})),
        getIncome(mcpUrl, mcpToken, [code], '2021-01-01', '2026-12-31').catch(() => ({})),
        getBalanceSheet(mcpUrl, mcpToken, [code]).catch(() => ({})),
        getCashFlow(mcpUrl, mcpToken, code, '2025-01-01', '2026-12-31').catch(() => ({})),
        getAdjustedQuotes(mcpUrl, mcpToken, [code], '2025-05-01', '2026-05-27').catch(() => ({})),
      ]);

      // Step 3: Extract data
      const incomeRows = extractRows(income);
      const bsRows = extractRows(balanceSheet);
      const cfRows = extractRows(cashFlow);
      const quoteRows = extractRows(quotes);

      const latestIncome = incomeRows[0] || {};
      const latestBS = bsRows[0] || {};
      const latestCF = cfRows[0] || {};

      const prices = quoteRows
        .map(q => ({ date: q.tradeDate || q.date, close: parseFloat(q.closePrice || q.close) }))
        .filter(p => !isNaN(p.close))
        .reverse();

      const high52 = prices.length ? Math.max(...prices.map(p => p.close)) : null;
      const low52 = prices.length ? Math.min(...prices.map(p => p.close)) : null;
      const latestPrice = prices.length ? prices[prices.length - 1].close : null;

      // Step 4: Validate
      const validationIssues = validateMCPData({
        high52, low52,
        pe: basicInfo?.peRatio || basicInfo?.pe,
        pb: basicInfo?.pbRatio || basicInfo?.pb,
        revenue: latestIncome?.revenue || latestIncome?.operatingRevenue,
        netIncome: latestIncome?.netProfit || latestIncome?.netIncome,
        grossMargin: latestIncome?.grossProfitMargin,
        totalAssets: latestBS?.totalAssets,
        totalLiabilities: latestBS?.totalLiabilities,
        equity: latestBS?.totalEquity || latestBS?.totalShareholdersEquity,
      });

      // Step 5: Chart data
      const years = incomeRows.map(r => (r.endDate || r.reportDate || '').slice(0, 4)).reverse();
      const revData = incomeRows.map(r => parseFloat(r.revenue || r.operatingRevenue || 0)).reverse();
      const profitData = incomeRows.map(r => parseFloat(r.netProfit || r.netIncome || 0)).reverse();
      const marginData = incomeRows.map(r => {
        if (r.grossProfitMargin != null) return parseFloat(r.grossProfitMargin);
        const rev = parseFloat(r.revenue || r.operatingRevenue || 0);
        const gp = parseFloat(r.grossProfit);
        if (rev > 0 && gp > 0) return (gp / rev * 100);
        const np = parseFloat(r.netProfit || r.netIncome);
        if (rev > 0 && np > 0) return (np / rev * 100);
        return null;
      }).reverse();

      // Step 6: Build prompt & call DeepSeek
      const prompt = buildPrompt({
        name: stockName, code, industry: basicInfo?.industry || stock.industry || '',
        marketCap: formatNum(basicInfo?.totalMarketCap),
        price: latestPrice, high52, low52,
        pe: basicInfo?.peRatio || basicInfo?.pe,
        pb: basicInfo?.pbRatio || basicInfo?.pb,
        years, revData, profitData, marginData,
        incomeRows,
        issues: validationIssues,
      });

      let report;
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          const raw = await deepseekReport(dsKey, prompt);
          report = raw;
          const v = validateReport(report);
          if (v.valid) break;
        } catch {
          if (attempt === 1) throw new Error('DeepSeek 生成失败，请重试');
        }
      }

      // Step 7: Generate slug and HTML
      const slug = makeSlug(stockName, code);
      const reportData = {
        company: stockName, code, industry: basicInfo?.industry || '',
        latestPrice, high52, low52, pe: basicInfo?.peRatio || basicInfo?.pe,
        pb: basicInfo?.pbRatio || basicInfo?.pb,
        slug,
        report: {
          executiveSummary: report?.executive_summary || '',
          sections: (report?.sections || []).map(s => ({ id: s.id, title: s.title, content: s.content })),
        },
        chartData: { years, revenue: revData, netIncome: profitData, grossMargin: marginData, marginData: marginData, prices },
      };

      const fullHTML = renderReportHTML(reportData);

      // Step 8: Save to KV
      await kv.put(`report:${slug}`, fullHTML, { expirationTtl: 86400 * 7 }); // 7 days

      // Step 9: Return report data including full HTML for frontend rendering
      return json({
        ok: true,
        company: stockName,
        code,
        slug,
        url: `/ai-analyst/${slug}.html`,
        html: fullHTML,
      });
    } catch (e) {
      return json({ error: `分析失败：${e.message}` }, 500);
    }
  },
};

/* ── helpers ── */

function extractRows(data) {
  if (Array.isArray(data)) return data;
  if (data?.data && Array.isArray(data.data)) return data.data;
  if (data?.data?.list && Array.isArray(data.data.list)) return data.data.list;
  if (data?.list && Array.isArray(data.list)) return data.list;
  return [];
}

function formatNum(v) {
  if (v == null) return null;
  const n = typeof v === 'string' ? parseFloat(v.replace(/,/g, '')) : v;
  if (isNaN(n)) return v;
  if (Math.abs(n) >= 1e8) return (n / 1e8).toFixed(2) + '亿';
  if (Math.abs(n) >= 1e4) return (n / 1e4).toFixed(2) + '万';
  return n.toFixed(2);
}

function makeSlug(name, code) {
  // Use stock code as base for uniqueness
  return `${code}-${new Date().getFullYear()}`;
}

function buildPrompt(d) {
  // Build richer prompt with multi-year data
  const _rows = d.incomeRows || [];
  const _years = d.years || [];
  const _rev = d.revData || [];
  const _profit = d.profitData || [];
  const _margin = d.marginData || [];
  const _latest = _rows[0] || {};
  let _tbl = '';
  if (_years.length) {
    _tbl = '\n## 历年财务数据\n\n| 年份 | 营收(万元) | 净利润(万元) | 毛利率 |\n|------|-----------|-------------|-------|\n';
    for (let _i = 0; _i < _years.length; _i++) {
      _tbl += '| ' + _years[_i] + ' | ' + (_rev[_i] != null ? Number(_rev[_i]).toLocaleString() : '—') + ' | ' + (_profit[_i] != null ? Number(_profit[_i]).toLocaleString() : '—') + ' | ' + (_margin[_i] != null ? _margin[_i].toFixed(1) + '%' : '—') + ' |\n';
    }
  }
  let _gr = '';
  if (_rev.length >= 2 && _rev[0] > 0 && _rev[1] > 0) {
    _gr = '营收YoY：' + ((_rev[0] - _rev[1]) / _rev[1] * 100).toFixed(1) + '%';
    if (_profit[0] > 0 && _profit[1] > 0) _gr += '，净利润YoY：' + ((_profit[0] - _profit[1]) / _profit[1] * 100).toFixed(1) + '%';
  }
  const _rStr = _rev.map(function(v){ return v != null ? formatNum(v) : '—'; }).join(' → ');
  const _pStr = _profit.map(function(v){ return v != null ? formatNum(v) : '—'; }).join(' → ');
  const _mStr = _margin.map(function(v){ return v != null ? v.toFixed(1) + '%' : '—'; }).join(' → ');

  return `请分析「${d.name}」（${d.code}）并生成深度研究报告。

## 公司信息
名称：${d.name}
股票代码：${d.code}
行业：${d.industry || '未知'}
市值：${d.marketCap || '未知'}

## 最新财务数据（最新报告期）
营收：${formatNum(_latest.revenue || _latest.operatingRevenue)}
净利润：${formatNum(_latest.netProfit || _latest.netIncome)}
毛利率：${_latest.grossProfitMargin != null ? _latest.grossProfitMargin + '%' : '—'}
净利率：${_latest.netProfitMargin != null ? _latest.netProfitMargin + '%' : '—'}
每股收益：${_latest.eps || _latest.basicEps || '—'}
${_gr ? '营收增长：' + _gr : ''}

## 历年财务趋势
营收逐年：${_rStr}
净利润逐年：${_pStr}
毛利率逐年：${_mStr}
${_tbl}

## 市场数据
最新价：${d.price != null ? d.price.toFixed(2) + '元' : '—'}
52周最高：${d.high52 != null ? d.high52.toFixed(2) + '元' : '—'}
52周最低：${d.low52 != null ? d.low52.toFixed(2) + '元' : '—'}
PE：${d.pe != null ? d.pe.toFixed(1) + 'x' : '—'}
PB：${d.pb != null ? d.pb.toFixed(2) + 'x' : '—'}
价格在52周区间位置：${d.high52 && d.low52 && d.price ? (( (d.price - d.low52) / (d.high52 - d.low52) * 100).toFixed(0) + '%') : '—'}

${d.issues?.length ? '## 数据异常\n' + d.issues.map(function(x,i){ return (i+1) + '. ' + x; }).join('\n') : '## 数据完整性\n所有数据均已通过合理性校验。'}`;
}

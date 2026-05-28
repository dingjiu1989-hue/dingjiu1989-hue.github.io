/** HTML report renderer — generates full report pages with markdown parsing, indicator grid, and charts */

export function renderReportHTML(data) {
  const co = escapeHtml(data.company || '');
  const code = escapeHtml(data.code || '');
  const slug = data.slug || 'report';
  const industry = escapeHtml(data.industry || '');
  const price = data.latestPrice;
  const pe = data.pe;
  const pb = data.pb;
  const high52 = data.high52;
  const low52 = data.low52;
  const execSummary = data.report?.executiveSummary || '';
  const sections = data.report?.sections || [];
  const chartData = data.chartData || {};
  const years = chartData.years || [];
  const revData = chartData.revenue || [];
  const profitData = chartData.netIncome || [];
  const marginData = chartData.grossMargin || [];
const hasMarginData = marginData.some(v => v != null && !isNaN(v));

  // -- Indicator grid data --
  const d3Price = price != null ? parseFloat(price).toFixed(2) : null;
  const d3Pe = pe != null ? parseFloat(pe).toFixed(1) + 'x' : null;
  const d3Pb = pb != null ? parseFloat(pb).toFixed(2) + 'x' : null;
  const pct = (price != null && high52 != null && low52 != null && high52 > low52)
    ? ((price - low52) / (high52 - low52) * 100).toFixed(0) : null;
  const d3Pos = pct != null ? pct + '%' : null;
  const d3Pct = pct != null ? parseFloat(pct) : 50;

  const sectionNav = sections.map((s, i) =>
    `<li><a href="#s${i+1}"><i class="fas fa-circle fa-fw" style="width:16px;color:#2563eb;font-size:.5rem;vertical-align:middle"></i> ${escapeHtml(s.title || '')}</a></li>`
  ).join('\n');

  const mobileOptions = sections.map((s, i) =>
    `<option value="s${i+1}">${escapeHtml(s.title || '')}</option>`
  ).join('\n');

  // Build price chart HTML (line chart)
  const prices = chartData.prices || [];
  const priceChartHtml = (prices.length >= 5)
    ? `<div class="chart-card">
  <div class="chart-header"><i class="fas fa-chart-line" style="color:#2563eb"></i> 价格走势</div>
  <div class="chart-body"><div class="chart-container"><canvas id="chartPrice"></canvas></div></div>
</div>
<script>
(function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
var _d=${JSON.stringify(prices.map(function(p){return p.date;}))};
var _c=${JSON.stringify(prices.map(function(p){return p.close;}))};
new Chart(document.getElementById('chartPrice'),{type:'line',data:{labels:_d,datasets:[{label:'收盘价（元）',data:_c,borderColor:'#2563eb',backgroundColor:'rgba(37,99,235,.08)',fill:true,tension:.3,pointRadius:2,pointHoverRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'}},x:{grid:{display:false},ticks:{maxTicksLimit:8}}}}});
})();
</script>` : '';

  // Indicator grid placed before technical analysis section
  const showInd = d3Price && d3Pe;
  const indGrid = showInd
    ? `<div class="chart-card">
  <div class="chart-header"><i class="fas fa-gauge-high" style="color:#2563eb"></i> 核心指标</div>
  <div class="chart-body">
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-label">PE</div><div class="stat-value">${d3Pe}</div><span class="indicator-signal signal-neutral">${pe > 50 ? '偏高' : pe < 15 ? '偏低' : '适中'}</span></div>
      <div class="stat-card"><div class="stat-label">PB</div><div class="stat-value">${d3Pb}</div><span class="indicator-signal signal-neutral">${pb > 5 ? '偏高' : pb < 1 ? '偏低' : '适中'}</span></div>
      <div class="stat-card"><div class="stat-label">52周位置</div><div class="stat-value">${d3Pos || '—'}</div><span class="indicator-signal ${d3Pct > 80 ? 'signal-sell' : d3Pct < 20 ? 'signal-buy' : 'signal-neutral'}">${d3Pct > 80 ? '高位' : d3Pct < 20 ? '低位' : '中位'}</span></div>
      <div class="stat-card"><div class="stat-label">当前价</div><div class="stat-value">¥${d3Price}</div><span class="indicator-signal ${d3Pct > 80 ? 'signal-sell' : d3Pct < 30 ? 'signal-buy' : 'signal-neutral'}">${d3Pct > 80 ? '关注回调' : d3Pct < 30 ? '关注反弹' : '区间震荡'}</span></div>
    </div>
  </div>
</div>` : '';

  // Render sections with markdown parsing
  const numLabels = ['一','二','三','四','五','六','七','八'];
  const sectionHTML = sections.map((s, i) => {
    const titles = ['公司概况','财务分析','技术分析','市场情绪','竞品对比','估值与财务健康度','主要风险','结论与建议'];
    const title = s.title || '';
    const extra = (i === 2) ? indGrid + priceChartHtml : '';
    return `
<h2 id="s${i+1}"><span class="section-num">${numLabels[i] || ''}</span>${escapeHtml(title.replace(/^[一二三四五六七八]、\s*/, ''))}</h2>
${extra}
${s.content ? parseMarkdown(s.content) : '<p>数据不足，暂无法生成该章节详细分析。</p>'}
`;
  }).join('\n');

  const badgeColor = '#1e3a5f';

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>${co}全面分析报告：AI 实时生成 — AI自习室</title>
  <meta name="description" content="深度分析${co}（${code}）：${industry}。AI 实时生成，覆盖财务、技术面、估值与风险分析。">
  <meta name="robots" content="noindex,follow">
  <link rel="canonical" href="https://aidev.fit/ai-analyst/analysis.html">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
  body{font-family:'Noto Sans SC','Inter',-apple-system,BlinkMacSystemFont,sans-serif;color:#1e293b;background:#f6f8fb;line-height:1.8;font-size:16px}
  .report-wrap{max-width:1100px;margin:0 auto;padding:20px;display:grid;grid-template-columns:220px 1fr;gap:32px}
  @media(max-width:1023px){.report-wrap{grid-template-columns:1fr}}
  .toc-sidebar{position:sticky;top:24px;height:fit-content;max-height:calc(100vh - 48px);overflow-y:auto}
  .toc-sidebar::-webkit-scrollbar{width:3px}
  .toc-sidebar::-webkit-scrollbar-thumb{background:#cbd5e1;border-radius:10px}
  @media(max-width:1023px){.toc-sidebar{display:none}}
  .toc-title{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:#64748b;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
  .toc-list{list-style:none;padding:0;margin:0}
  .toc-list li{margin-bottom:2px}
  .toc-list a{display:block;padding:6px 10px;border-radius:6px;font-size:.8rem;color:#64748b;text-decoration:none;transition:all .15s;line-height:1.3}
  .toc-list a:hover{background:#e8edf5;color:#2563eb}
  .mobile-toc{display:none}
  @media(max-width:1023px){.mobile-toc{display:block;background:#fff;border-radius:12px;padding:16px 20px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
  .mobile-toc select{width:100%;padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;font-size:.88rem;background:#fff;appearance:auto;color:#1e293b}}
  .article-card{background:#fff;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:48px 56px;margin-bottom:24px}
  @media(max-width:768px){.article-card{padding:24px 20px;border-radius:0}}
  h1.report-title{font-size:2.2rem;font-weight:900;color:#0f172a;line-height:1.2;text-align:center;letter-spacing:-.02em;margin-bottom:8px}
  h2{font-size:1.5rem!important;font-weight:700!important;color:#0f172a!important;margin-top:48px!important;margin-bottom:20px!important;padding-bottom:12px;border-bottom:3px solid #2563eb;display:flex;align-items:center;gap:10px}
  h2 .section-num{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;background:#2563eb;color:#fff;font-size:.85rem;font-weight:700;flex-shrink:0}
  h3{font-size:1.2rem!important;font-weight:600!important;color:#0f172a!important;margin-top:28px!important;margin-bottom:12px!important;padding-left:12px;border-left:3px solid #2563eb}
  p{font-size:1rem!important;margin-bottom:1.2em!important;color:#1e293b}
  .badge-row{display:flex;justify-content:center;gap:8px;margin-bottom:20px;flex-wrap:wrap}
  .badge{display:inline-block;padding:4px 14px;font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;border-radius:999px}
  .report-meta{text-align:center;margin:16px 0 32px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap}
  .report-meta span{font-size:.85rem;color:#64748b}
  .report-meta strong{color:#1e293b}
  .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:20px 0}
  .stat-card{background:#f8faff;border:1px solid #e2e8f0;border-radius:8px;padding:14px 12px;text-align:center}
  .stat-label{font-size:.72rem;color:#64748b;margin-bottom:4px}
  .stat-value{font-size:1.1rem;font-weight:700;color:#1e293b}
  .chart-card{background:#fafcff;border:1px solid #e2e8f0;border-radius:12px;margin:24px 0;overflow:hidden}
  .chart-header{padding:14px 20px;border-bottom:1px solid #e2e8f0;font-size:.8rem;font-weight:600;color:#64748b;display:flex;align-items:center;gap:8px;background:#f8faff}
  .chart-body{padding:24px}
  .chart-body .chart-container{position:relative;height:280px;width:100%}
  .chart-caption{font-size:.75rem;color:#94a3b8;text-align:center;margin-top:12px}
  .exec-box{background:#f0f7ff;border:1px solid #dbeafe;border-radius:12px;padding:24px;margin-bottom:28px}
  .exec-box .label{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#2563eb;margin-bottom:12px}
  .exec-box p{font-size:.9rem!important;color:#1e40af!important;margin-bottom:.8em!important;line-height:1.7}
  .disclaimer-box{margin-top:3rem;padding:1.5rem;background:#f9fafb;border-radius:10px;border:1px solid #e5e7eb;font-size:.8rem;color:#6b7280;line-height:1.6}
  .disclaimer-box p{font-size:.8rem!important;color:#6b7280!important;margin-bottom:0!important}
  .btt-btn{position:fixed;bottom:32px;right:32px;width:44px;height:44px;border-radius:50%;background:#2563eb;color:#fff;border:none;font-size:1.1rem;cursor:pointer;box-shadow:0 4px 12px rgba(37,99,235,.35);opacity:0;visibility:hidden;transition:all .2s;z-index:50;display:flex;align-items:center;justify-content:center}
  .btt-btn.show{opacity:1;visibility:visible}
  @media(max-width:768px){h1.report-title{font-size:1.5rem!important}h2{font-size:1.2rem!important}h3{font-size:1.05rem!important}p{font-size:.9rem!important}.article-card{padding:20px 16px}}
  .indicator-signal{display:inline-block;font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:99px;margin-top:4px}
  .signal-buy{background:#d1fae5;color:#065f46}
  .signal-sell{background:#fee2e2;color:#991b1b}
  .signal-neutral{background:#e5e7eb;color:#374151}
  ol,ul{margin:1em 0!important;padding-left:1.75rem!important}
  ol li,ul li{margin-bottom:.6em!important;line-height:1.7!important}
  ol{list-style:decimal!important}
  ul{list-style:disc!important}
  table{border-collapse:collapse;margin:1.5em 0!important;font-size:.9rem;width:100%}
  th,td{border:1px solid #e2e8f0;padding:8px 12px;text-align:left}
  th{background:#f8faff;font-weight:600;color:#475569}
  tr:nth-child(even){background:#fafcff}
  </style>
</head>
<body class="bg-gray-50">
<div id="nav-placeholder"></div>
<div class="report-wrap">
  <nav class="toc-sidebar" aria-label="目录">
    <div class="toc-title">目录</div>
    <ul class="toc-list">
      ${sectionNav}
    </ul>
  </nav>
  <div class="report-content">
    <div class="mobile-toc">
      <select onchange="if(this.value)document.getElementById(this.value).scrollIntoView({behavior:'smooth'});this.selectedIndex=0;">
        <option value="">— 跳转到章节 —</option>
        ${mobileOptions}
      </select>
    </div>
    <article class="article-card">
      <header>
        <div class="badge-row">
          <span class="badge" style="background:#0f172a;color:#fff">Deep Research</span>
          <span class="badge" style="background:${badgeColor};color:#fff">${escapeHtml(co)}</span>
          <span class="badge" style="background:#e8edf5;color:#475569">${escapeHtml(code)}</span>
        </div>
        <h1 class="report-title">${escapeHtml(co)}全面分析报告：AI 实时生成</h1>
        <div class="report-meta">
          <span><strong>日期</strong> / <script>document.write(new Date().toLocaleDateString('zh-CN'))</script></span>
          <span><strong>行业</strong> / ${escapeHtml(industry || '金融')}</span>
          <span><strong>来源</strong> / AI 实时生成</span>
        </div>
      </header>

      ${execSummary ? `<div class="exec-box"><div class="label"><i class="fas fa-bolt" style="margin-right:4px"></i> 核心摘要</div>${parseMarkdown(execSummary)}</div>` : ''}

      <div class="stat-grid">
        ${price != null ? `<div class="stat-card"><div class="stat-label">最新价</div><div class="stat-value">¥${parseFloat(price).toFixed(2)}</div></div>` : ''}
        ${pe != null ? `<div class="stat-card"><div class="stat-label">PE</div><div class="stat-value">${parseFloat(pe).toFixed(1)}x</div></div>` : ''}
        ${pb != null ? `<div class="stat-card"><div class="stat-label">PB</div><div class="stat-value">${parseFloat(pb).toFixed(2)}x</div></div>` : ''}
        ${high52 != null ? `<div class="stat-card"><div class="stat-label">52周最高</div><div class="stat-value">¥${parseFloat(high52).toFixed(2)}</div></div>` : ''}
        ${low52 != null ? `<div class="stat-card"><div class="stat-label">52周最低</div><div class="stat-value">¥${parseFloat(low52).toFixed(2)}</div></div>` : ''}
      </div>

      ${sectionHTML}

      ${chartData.years && chartData.years.length >= 3 ? `
      <div class="chart-card">
        <div class="chart-header"><i class="fas fa-chart-bar" style="color:#2563eb"></i> 营收与净利润趋势</div>
        <div class="chart-body"><div class="chart-container"><canvas id="chartIncome"></canvas></div><p class="chart-caption">数据来源：MCP 股票数据服务</p></div>
      </div>
      <script>
      (function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
      new Chart(document.getElementById('chartIncome'),{type:'bar',data:{labels:${JSON.stringify(years)},datasets:[{label:'营收（亿元）',data:${JSON.stringify(revData)},backgroundColor:'rgba(37,99,235,.75)',borderRadius:6,barPercentage:.6},{label:'净利润（亿元）',data:${JSON.stringify(profitData)},backgroundColor:'rgba(16,185,129,.75)',borderRadius:6,barPercentage:.6}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{boxWidth:12,padding:16}}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'}},x:{grid:{display:false}}}}});
      })();
      </script>
      ` : ''}

      ${hasMarginData && years.length >= 3 ? `
      <div class="chart-card">
        <div class="chart-header"><i class="fas fa-percentage" style="color:#059669"></i> 毛利率趋势</div>
        <div class="chart-body"><div class="chart-container"><canvas id="chartMargin"></canvas></div></div>
      </div>
      <script>
      (function(){if(typeof Chart==='undefined'){setTimeout(arguments.callee,100);return;}
      new Chart(document.getElementById('chartMargin'),{type:'line',data:{labels:${JSON.stringify(years)},datasets:[{label:'毛利率（%）',data:${JSON.stringify(marginData)},borderColor:'#059669',backgroundColor:'rgba(5,150,105,.1)',fill:true,tension:.3,pointRadius:4,pointBackgroundColor:'#059669'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false,grid:{color:'rgba(0,0,0,.04)'},ticks:{callback:function(v){return v+'%'}}},x:{grid:{display:false}}}}});
      })();
      </script>
      ` : ''}

      <div class="disclaimer-box">
        <p><strong>免责声明：</strong>本报告由AI自动生成，仅供参考和学习交流，不构成任何形式的投资建议。报告中的数据和分析基于公开信息和模型估算，可能存在偏差。股市有风险，投资需谨慎。作者和平台不对因使用本报告而产生的任何损失承担责任。</p>
      </div>
    </article>
    <div id="footer-placeholder"></div>
  </div>
</div>

<button class="btt-btn" id="bttBtn" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="返回顶部"><i class="fas fa-arrow-up"></i></button>
<script>
window.addEventListener('scroll',function(){document.getElementById('bttBtn').classList.toggle('show',window.scrollY>400)});
</script>
<script src="/js/include.js"></script>
<script src="/js/render.js"></script>
<script src="/js/cookie-banner.js"></script>
</body>
</html>`;
}

/**
 * Parse basic markdown → HTML
 * Supports: ### headings, **bold**, - lists, 1. numbered lists, | tables |
 */
function parseMarkdown(text) {
  if (!text) return '';
  const lines = text.split('\n');
  const out = [];
  let inUl = false, inOl = false, inTable = false;
  for (let i = 0; i < lines.length; i++) {
    const raw = lines[i];
    const trimmed = raw.trim();

    // Empty line — close any open list/table
    if (!trimmed) {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inOl) { out.push('</ol>'); inOl = false; }
      if (inTable) { out.push('</tbody></table>'); inTable = false; }
      continue;
    }

    // ### Heading
    if (/^###\s/.test(trimmed)) {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inOl) { out.push('</ol>'); inOl = false; }
      if (inTable) { out.push('</tbody></table>'); inTable = false; }
      out.push('<h3>' + inlineMd(escapeHtml(trimmed.replace(/^###\s+/, ''))) + '</h3>');
      continue;
    }

    // Table row |...|
    if (/^\|.+\|$/.test(trimmed) && !/^\|[\s-:]+\|/.test(trimmed)) {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inOl) { out.push('</ol>'); inOl = false; }
      const _c = trimmed.split('|').filter(Boolean).map(function(x){ return inlineMd(escapeHtml(x.trim())); });
      const _h = (i + 1 < lines.length) && /^\|[\s\-:|]+\|$/.test(lines[i + 1].trim());
      if (_h) {
        if (inTable) { out.push('</tbody></table>'); }
        out.push('<table><thead><tr>' + _c.map(function(x){return '<th>'+x+'</th>';}).join('') + '</tr></thead><tbody>');
        inTable = true;
        i++;
      } else if (inTable) {
        out.push('<tr>' + _c.map(function(x){return '<td>'+x+'</td>';}).join('') + '</tr>');
      } else {
        out.push('<table><tbody><tr>' + _c.map(function(x){return '<td>'+x+'</td>';}).join('') + '</tr></tbody></table>');
      }
      continue;
    }

    // Unordered list
    if (/^[-*]\s/.test(trimmed)) {
      if (inOl) { out.push('</ol>'); inOl = false; }
      if (inTable) { out.push('</tbody></table>'); inTable = false; }
      if (!inUl) { out.push('<ul>'); inUl = true; }
      out.push('<li>' + inlineMd(escapeHtml(trimmed.replace(/^[-*]\s+/, ''))) + '</li>');
      continue;
    }

    // Ordered list
    if (/^\d+[.)]\s/.test(trimmed)) {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inTable) { out.push('</tbody></table>'); inTable = false; }
      if (!inOl) { out.push('<ol>'); inOl = true; }
      out.push('<li>' + inlineMd(escapeHtml(trimmed.replace(/^\d+[.)]\s+/, ''))) + '</li>');
      continue;
    }

    // Regular paragraph
    if (inUl) { out.push('</ul>'); inUl = false; }
    if (inOl) { out.push('</ol>'); inOl = false; }
    if (inTable) { out.push('</tbody></table>'); inTable = false; }
    out.push('<p>' + inlineMd(escapeHtml(trimmed)) + '</p>');
  }
  if (inUl) out.push('</ul>');
  if (inOl) out.push('</ol>');
  if (inTable) out.push('</tbody></table>');
  return out.join('\n');
}

/** Inline markdown: **bold** */
function inlineMd(text) {
  return text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
}

function escapeHtml(str) {
  if (str == null) return '';
  return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

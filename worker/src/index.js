import { searchStock, getBasicInfo, getIncome, getBalanceSheet, getCashFlow, getAdjustedQuotes } from './mcp.js';
import { deepseekReport } from './deepseek.js';
import { validateMCPData, validateReport } from './validator.js';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...CORS, 'Content-Type': 'application/json' },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS });
    if (request.method !== 'POST') {
      return json({ error: '仅支持 POST' }, 405);
    }

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
    const url = env.MCP_URL;
    const token = env.MCP_TOKEN;
    const dsKey = env.DEEPSEEK_KEY;

    if (!url || !token) return json({ error: 'MCP 未配置' }, 500);
    if (!dsKey) return json({ error: 'DeepSeek API Key 未配置' }, 500);

    try {
      // Step 1: Search stock code
      const searchResult = await searchStock(url, token, name);
      const stocks = extractRows(searchResult);
      if (!stocks.length) {
        return json({ error: `未找到「${name}」的股票代码，可能暂未覆盖` }, 404);
      }
      const stock = stocks[0];
      const code = String(stock.code || stock.stockCode || '').replace(/\.SZ|\.SH/gi, '');
      const stockName = stock.shortName || stock.stockName || stock.name || name;

      // Step 2: Get financial data
      const [basicInfo, income, balanceSheet, cashFlow, quotes] = await Promise.all([
        getBasicInfo(url, token, code).catch(() => ({})),
        getIncome(url, token, [code], '2021-01-01', '2026-12-31').catch(() => ({})),
        getBalanceSheet(url, token, [code]).catch(() => ({})),
        getCashFlow(url, token, code, '2025-01-01', '2026-12-31').catch(() => ({})),
        getAdjustedQuotes(url, token, [code], '2025-05-01', '2026-05-27').catch(() => ({})),
      ]);

      // Step 3: Extract and structure data
      const incomeRows = extractRows(income);
      const bsRows = extractRows(balanceSheet);
      const cfRows = extractRows(cashFlow);
      const quoteRows = extractRows(quotes);

      const latestIncome = incomeRows[0] || {};
      const latestBS = bsRows[0] || {};
      const latestCF = cfRows[0] || {};

      // Price data — ensure ascending order
      const prices = quoteRows
        .map(q => ({
          date: q.tradeDate || q.date,
          close: parseFloat(q.closePrice || q.close),
        }))
        .filter(p => !isNaN(p.close))
        .reverse();

      const high52 = prices.length ? Math.max(...prices.map(p => p.close)) : null;
      const low52 = prices.length ? Math.min(...prices.map(p => p.close)) : null;
      const latestPrice = prices.length ? prices[prices.length - 1].close : null;

      // Validate
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

      // Step 4: Build financial chart data
      const years = incomeRows.map(r => (r.endDate || r.reportDate || '').slice(0, 4)).reverse();
      const revData = incomeRows.map(r => parseFloat(r.revenue || r.operatingRevenue || 0)).reverse();
      const profitData = incomeRows.map(r => parseFloat(r.netProfit || r.netIncome || 0)).reverse();
      const marginData = incomeRows.map(r => parseFloat(r.grossProfitMargin || 0) || null).reverse();

      // Step 5: Build prompt for DeepSeek
      const prompt = buildPrompt({
        name: stockName,
        code,
        industry: basicInfo?.industry || stock.industry || '',
        marketCap: formatNum(basicInfo?.totalMarketCap),
        employees: basicInfo?.totalEmployees,
        revenue: latestIncome?.revenue || latestIncome?.operatingRevenue,
        revenueHistory: revData.map((v, i) => `${years[i]}: ${formatNum(v)}`).join('；'),
        netIncome: latestIncome?.netProfit || latestIncome?.netIncome,
        profitHistory: profitData.map((v, i) => `${years[i]}: ${formatNum(v)}`).join('；'),
        grossMargin: latestIncome?.grossProfitMargin,
        netMargin: latestIncome?.netProfitMargin,
        eps: latestIncome?.eps || latestIncome?.basicEps,
        totalAssets: latestBS?.totalAssets,
        totalLiabilities: latestBS?.totalLiabilities,
        equity: latestBS?.totalEquity || latestBS?.totalShareholdersEquity,
        debtRatio: latestBS?.totalLiabilities && latestBS?.totalAssets
          ? ((latestBS.totalLiabilities / latestBS.totalAssets) * 100).toFixed(1) + '%' : null,
        operatingCF: latestCF?.operatingCashFlow || latestCF?.netCashFromOperations,
        investingCF: latestCF?.investingCashFlow,
        financingCF: latestCF?.financingCashFlow,
        price: latestPrice,
        high52,
        low52,
        pe: basicInfo?.peRatio || basicInfo?.pe,
        pb: basicInfo?.pbRatio || basicInfo?.pb,
        issues: validationIssues,
        years,
        revData,
        profitData,
        marginData,
      });

      // Step 6: Call DeepSeek (with retry)
      let report;
      for (let attempt = 0; attempt < 2; attempt++) {
        try {
          const raw = await deepseekReport(dsKey, prompt);
          report = raw;
          const v = validateReport(report);
          if (v.valid) break;
          if (attempt === 0) continue; // retry once
          report.sections = report.sections || [];
          for (const id of v.missing || []) {
            report.sections.push({ id, title: sectionTitle(id), content: '数据不足，暂无法生成该章节详细分析。' });
          }
        } catch (e) {
          if (attempt === 1) throw e;
        }
      }

      // Step 7: Return structured response
      return json({
        ok: true,
        company: stockName,
        code: code,
        industry: basicInfo?.industry || '',
        marketCap: formatNum(basicInfo?.totalMarketCap),
        latestPrice,
        high52,
        low52,
        pe: basicInfo?.peRatio || basicInfo?.pe,
        pb: basicInfo?.pbRatio || basicInfo?.pb,
        validationIssues: validationIssues.length ? validationIssues : undefined,
        chartData: {
          years,
          revenue: revData,
          netIncome: profitData,
          grossMargin: marginData,
        },
        report: {
          executiveSummary: report?.executive_summary || '',
          sections: (report?.sections || []).map(s => ({
            id: s.id,
            title: s.title,
            content: s.content,
          })),
        },
        _sources: ['mcp', 'deepseek'],
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

function sectionTitle(id) {
  const map = { s1: '公司概况', s2: '财务分析', s3: '技术分析', s4: '市场情绪', s5: '竞品对比', s6: '估值与财务健康度', s7: '主要风险', s8: '结论与建议' };
  return map[id] || '';
}

function buildPrompt(d) {
  return `请分析「${d.name}」并生成深度研究报告。

## 公司信息
- 名称：${d.name}（${d.code}）
- 行业：${d.industry || '未知'}
- 市值：${d.marketCap || '未知'}
- 员工：${d.employees || '未知'}

## 最新财务数据
- 营收：${formatNum(d.revenue)}
- 营收趋势：${d.revenueHistory}
- 净利润：${formatNum(d.netIncome)}
- 净利润趋势：${d.profitHistory}
- 毛利率：${d.grossMargin || '暂缺'}
- 净利率：${d.netMargin || '暂缺'}
- 每股收益：${d.eps || '暂缺'}

## 资产负债
- 总资产：${formatNum(d.totalAssets)}
- 总负债：${formatNum(d.totalLiabilities)}
- 净资产：${formatNum(d.equity)}
- 资产负债率：${d.debtRatio || '暂缺'}

## 现金流
- 经营现金流：${formatNum(d.operatingCF)}
- 投资现金流：${formatNum(d.investingCF)}
- 筹资现金流：${formatNum(d.financingCF)}

## 市场数据
- 最新价：${d.price}
- 52周最高：${d.high52}
- 52周最低：${d.low52}
- PE：${d.pe}
- PB：${d.pb}

${d.issues?.length ? `## 数据提示\n以下数据异常请酌情处理：\n${d.issues.map(i => `- ${i}`).join('\n')}` : ''}`;
}

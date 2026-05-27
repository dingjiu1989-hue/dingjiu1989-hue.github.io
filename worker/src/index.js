import { searchStock, getBasicInfo, getIncome, getBalanceSheet, getCashFlow, getAdjustedQuotes } from './mcp.js';
import { buildAnalysis, buildFallback } from './template.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') return new Response(null, { headers: CORS_HEADERS });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405 });

    try {
      const { company } = await request.json();
      if (!company || typeof company !== 'string' || company.trim().length === 0) {
        return json({ error: '请输入公司名称' }, 400, CORS_HEADERS);
      }
      if (company.length > 200) {
        return json({ error: '公司名称过长' }, 400, CORS_HEADERS);
      }

      const { MCP_URL, MCP_TOKEN } = env;
      if (!MCP_URL || !MCP_TOKEN) {
        return json({ error: '服务配置异常' }, 500, CORS_HEADERS);
      }

      // Step 1: Search MCP for stock code
      let searchResult;
      try {
        searchResult = await searchStock(MCP_URL, MCP_TOKEN, company.trim());
      } catch (e) {
        return json({ error: `未找到「${company}」的数据`, analysis: buildFallback(company) }, 200, CORS_HEADERS);
      }

      // Extract stock code from search results
      const items = Array.isArray(searchResult) ? searchResult : (searchResult?.data?.list || [searchResult].filter(Boolean));
      if (!items.length) {
        return json({ error: `未找到「${company}」的数据`, analysis: buildFallback(company) }, 200, CORS_HEADERS);
      }

      const first = items[0];
      const stockCode = first.stockCode || first.code || first.secCode;
      if (!stockCode) {
        return json({ error: `未找到「${company}」的股票代码`, analysis: buildFallback(company) }, 200, CORS_HEADERS);
      }

      // Step 2: Get basic info for company overview
      const basicInfo = await getBasicInfo(MCP_URL, MCP_TOKEN, stockCode);

      // Step 3: Get financial data (last 2 years)
      const endDate = '2026-05-27';
      const beginDate = '2024-01-01';

      const [income, balanceSheet, cashFlow, quotes] = await Promise.all([
        getIncome(MCP_URL, MCP_TOKEN, stockCode, beginDate, endDate).catch(() => null),
        getBalanceSheet(MCP_URL, MCP_TOKEN, stockCode).catch(() => null),
        getCashFlow(MCP_URL, MCP_TOKEN, stockCode, beginDate, endDate).catch(() => null),
        getAdjustedQuotes(MCP_URL, MCP_TOKEN, stockCode, '2025-05-27', endDate).catch(() => null),
      ]);

      // Step 4: Build analysis
      const analysis = buildAnalysis(company.trim(), basicInfo, income, balanceSheet, cashFlow, quotes);

      return json({ ok: true, analysis }, 200, CORS_HEADERS);

    } catch (e) {
      return json({ error: e.message || '分析请求失败' }, 500, CORS_HEADERS);
    }
  },
};

function json(data, status, headers) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...headers, 'Content-Type': 'application/json' },
  });
}

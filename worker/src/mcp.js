/** MCP client — JSON-RPC 2.0 over streamableHttp */

async function callTool(url, token, name, args) {
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name, arguments: args } }),
  });
  if (!resp.ok) throw new Error(`MCP HTTP ${resp.status}`);
  const d = await resp.json();
  if (d.error) throw new Error(`MCP error: ${d.error.message}`);
  const text = d.result?.content?.[0]?.text;
  if (!text) throw new Error(`Empty MCP response for: ${name}`);
  let parsed;
  try { parsed = JSON.parse(text); } catch { return { raw: text }; }
  // Unwrap { code, data, message } envelope from DashScope MCP
  if (parsed && typeof parsed === 'object' && !Array.isArray(parsed) && 'code' in parsed && 'data' in parsed) {
    return parsed.data;
  }
  return parsed;
}

function a(v) { return Array.isArray(v) ? v : [v]; }

export async function searchStock(url, token, q) { return callTool(url, token, 'search', { key: q, type: '11', pageSize: 5 }); }
export async function getBasicInfo(url, token, code) { return callTool(url, token, 'get_stock_basic_info', { stockCode: code }); }
export async function getIncome(url, token, codes, b, e) { return callTool(url, token, 'list_stock_income_statements', { stockCodes: a(codes), beginDate: b, endDate: e, pageSize: 500 }); }
export async function getBalanceSheet(url, token, codes) { return callTool(url, token, 'list_stock_balance_sheet', { stockCodes: a(codes), pageSize: 500 }); }
export async function getCashFlow(url, token, code, b, e) { return callTool(url, token, 'list_stock_cash_flows', { stockCode: code, beginDate: b, endDate: e, pageSize: 500 }); }
export async function getAdjustedQuotes(url, token, codes, b, e) { return callTool(url, token, 'list_stock_adjusted_quotes', { stockCodes: a(codes), beginDate: b, endDate: e, pageSize: 500 }); }

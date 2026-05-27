/** Template builder: MCP data → structured analysis JSON */

export function buildAnalysis(company, basicInfo, income, balanceSheet, cashFlow, quotes) {
  // Extract latest year income statement
  const incomeRows = Array.isArray(income) ? income : (income?.data?.list || []);
  const latestIncome = incomeRows[0] || {};

  // Extract latest balance sheet
  const bsRows = Array.isArray(balanceSheet) ? balanceSheet : (balanceSheet?.data?.list || []);
  const latestBS = bsRows[0] || {};

  // Extract cash flow
  const cfRows = Array.isArray(cashFlow) ? cashFlow : (cashFlow?.data?.list || []);
  const latestCF = cfRows[0] || {};

  // Extract quotes for price data
  const quoteRows = Array.isArray(quotes) ? quotes : (quotes?.data?.list || []);
  const prices = quoteRows.map(q => ({
    date: q.tradeDate || q.date,
    close: q.closePrice || q.close,
  })).filter(p => p.close).reverse();
  const high52 = prices.length ? Math.max(...prices.map(p => p.close)) : null;
  const low52 = prices.length ? Math.min(...prices.map(p => p.close)) : null;
  const latestPrice = prices.length ? prices[prices.length - 1].close : null;

  return {
    company: {
      name: basicInfo?.stockName || company,
      code: basicInfo?.stockCode || '',
      sector: basicInfo?.industry || '',
      marketCap: formatNum(latestBS?.totalMarketCap || basicInfo?.totalMarketCap),
      employees: basicInfo?.totalEmployees,
    },
    financials: {
      revenue: formatNum(latestIncome?.revenue || latestIncome?.operatingRevenue),
      revenueGrowth: latestIncome?.revenueGrowth || latestIncome?.operatingRevenueGrowth,
      netIncome: formatNum(latestIncome?.netProfit || latestIncome?.netIncome),
      netIncomeGrowth: latestIncome?.netProfitGrowth,
      grossMargin: latestIncome?.grossProfitMargin,
      netMargin: latestIncome?.netProfitMargin,
      eps: latestIncome?.eps || latestIncome?.basicEps,
      period: latestIncome?.endDate || latestIncome?.reportDate,
    },
    balanceSheet: {
      totalAssets: formatNum(latestBS?.totalAssets),
      totalLiabilities: formatNum(latestBS?.totalLiabilities),
      equity: formatNum(latestBS?.totalEquity || latestBS?.totalShareholdersEquity),
      debtRatio: latestBS?.totalLiabilities && latestBS?.totalAssets
        ? round((latestBS.totalLiabilities / latestBS.totalAssets) * 100) + '%' : null,
    },
    cashFlow: {
      operating: formatNum(latestCF?.operatingCashFlow || latestCF?.netCashFromOperations),
      investing: formatNum(latestCF?.investingCashFlow),
      financing: formatNum(latestCF?.financingCashFlow),
    },
    marketData: {
      latestPrice,
      high52,
      low52,
      pe: basicInfo?.peRatio || basicInfo?.pe,
      pb: basicInfo?.pbRatio || basicInfo?.pb,
    },
    summary: buildSummary(basicInfo, latestIncome, latestBS),
    _sources: ['mcp'],
  };
}

export function buildFallback(company) {
  return {
    company: { name: company, code: '', sector: '', marketCap: null },
    financials: null,
    balanceSheet: null,
    cashFlow: null,
    marketData: null,
    summary: `「${company}」暂未覆盖。当前数据源（阿里云MCP股票数据服务）主要覆盖沪深京A/B股、港股和基金，暂不支持该公司所属市场。`,
    _sources: [],
  };
}

function buildSummary(info, income, bs) {
  const parts = [];
  if (info?.stockName) parts.push(`${info.stockName}（${info.stockCode || ''}）`);
  if (info?.industry) parts.push(`所属${info.industry}行业`);
  if (income?.revenue) parts.push(`最新报告期营收${formatNum(income.revenue)}`);
  if (income?.netProfit) parts.push(`净利润${formatNum(income.netProfit)}`);
  if (income?.grossProfitMargin) parts.push(`毛利率${income.grossProfitMargin}`);
  return parts.join('。') + '。';
}

function formatNum(v) {
  if (v == null) return null;
  const n = typeof v === 'string' ? parseFloat(v.replace(/,/g, '')) : v;
  if (isNaN(n)) return v;
  if (Math.abs(n) >= 1e8) return round(n / 1e8) + '亿';
  if (Math.abs(n) >= 1e4) return round(n / 1e4) + '万';
  return round(n);
}

function round(n) { return Math.round(n * 100) / 100; }

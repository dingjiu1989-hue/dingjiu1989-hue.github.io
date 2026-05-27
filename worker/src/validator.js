/** Data and output validation */

export function validateMCPData(data) {
  const issues = [];

  // Price sanity
  if (data.high52 != null && data.low52 != null && data.high52 <= data.low52) {
    issues.push('52-week high <= low');
  }

  // PE sanity
  if (data.pe != null && (data.pe < 0 || data.pe > 500)) {
    issues.push(`PE ${data.pe} 异常`);
  }
  if (data.pb != null && (data.pb < 0 || data.pb > 100)) {
    issues.push(`PB ${data.pb} 异常`);
  }

  // Income sanity
  if (data.revenue != null && data.netIncome != null) {
    if (data.revenue > 0 && data.netIncome > 0 && data.revenue < data.netIncome) {
      issues.push('营收 < 净利润，可能单位不一致');
    }
  }

  // Margin
  if (data.grossMargin != null) {
    const gm = parseFloat(data.grossMargin);
    if (gm < -50 || gm > 100) issues.push(`毛利率 ${gm}% 异常`);
  }

  // Balance sheet
  if (data.totalAssets != null && data.totalLiabilities != null && data.equity != null) {
    const diff = Math.abs(data.totalAssets - data.totalLiabilities - data.equity);
    if (data.totalAssets > 0 && diff / data.totalAssets > 0.1) {
      issues.push(`资产负债表勾稽差异 ${(diff / data.totalAssets * 100).toFixed(1)}%`);
    }
  }

  return issues;
}

export function validateReport(report) {
  if (!report || typeof report !== 'object') return { valid: false, error: '空响应' };

  const required = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8'];
  const sections = report.sections || [];
  const ids = sections.map(s => s.id);

  const missing = required.filter(id => !ids.includes(id));
  if (missing.length) return { valid: false, error: `缺少章节: ${missing.join(', ')}` };

  const emptyContent = sections.filter(s => !s.content || s.content.trim().length < 20);
  if (emptyContent.length) {
    return { valid: false, error: `章节内容过短: ${emptyContent.map(s => s.id).join(', ')}` };
  }

  return { valid: true, error: null };
}

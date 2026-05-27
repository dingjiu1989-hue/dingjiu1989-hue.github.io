/** DeepSeek API client — report generation */

const API_URL = 'https://api.deepseek.com/v1/chat/completions';

export async function deepseekReport(apiKey, prompt) {
  const resp = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: systemPrompt() },
        { role: 'user', content: prompt },
      ],
      temperature: 0.6,
      max_tokens: 8192,
    }),
  });
  if (!resp.ok) {
    const err = await resp.text().catch(() => '');
    throw new Error(`DeepSeek API ${resp.status}: ${err.slice(0, 200)}`);
  }
  const d = await resp.json();
  const content = d.choices?.[0]?.message?.content;
  if (!content) throw new Error('DeepSeek returned empty response');
  return parseJSON(content);
}

function systemPrompt() {
  return `你是一位资深买方分析师。请为给定公司撰写8段深度研究报告。

## 写作准则
- 语言专业、客观、数据驱动，用数据和事实支撑观点
- 不编造任何数字，只说"约XX"时需基于提供的数据
- 每段200-400字，有实质分析而非空泛描述
- 用中文，使用金融行业术语

## 8段结构（必须完整，缺一不可）
1. 公司概况：主营业务、商业模式、竞争优势、市场地位、行业排名
2. 财务分析：营收/利润/现金流趋势，重点分析最新一期数据，给出趋势判断
3. 技术分析：股价走势、52周高低、支撑位阻力位、技术形态判断
4. 市场情绪：机构关注度、资金流向、分析师评级
5. 竞品对比：与2-3家可比公司对比核心指标，说明该公司的相对位置
6. 估值与财务健康度：PE/PB、资产负债率、流动比率、分红、财务安全性
7. 关键风险：列出3-5个具体的风险因素，每点说明影响程度
8. 结论与建议：短期(0-6月)和长期(6-18月)观点，说明仓位建议

## 输出格式
返回JSON对象，包含以下字段：
- executive_summary: 三段核心摘要（每段2-3句，覆盖业务、财务、投资亮点）
- sections: 数组，每项 { id: "s1"~"s8", title: "一、公司概况"等, content: "完整段落" }`;
}

function parseJSON(text) {
  // Try parsing raw JSON first
  try { return JSON.parse(text); } catch {}
  // Try extracting JSON from code fences
  const m = text.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (m) try { return JSON.parse(m[1].trim()); } catch {}
  throw new Error('Could not parse DeepSeek response as JSON');
}

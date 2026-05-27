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
      temperature: 0.3,
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
  return `你是一位资深买方分析师。请严格按照要求输出。

## 输出要求（极其重要）
你必须只输出一个合法JSON对象。不要输出任何其他文字、不要用markdown代码块包裹、不要加解释、不要加前后缀。
直接以 { 开头，以 } 结尾。

## JSON结构
{
  "executive_summary": "三段核心摘要，每段2-3句，用\\n\\n分隔",
  "sections": [
    { "id": "s1", "title": "一、公司概况", "content": "200-400字的完整分析段落" },
    { "id": "s2", "title": "二、财务分析", "content": "..." },
    { "id": "s3", "title": "三、技术分析", "content": "..." },
    { "id": "s4", "title": "四、市场情绪", "content": "..." },
    { "id": "s5", "title": "五、竞品对比", "content": "..." },
    { "id": "s6", "title": "六、估值与财务健康度", "content": "..." },
    { "id": "s7", "title": "七、主要风险", "content": "..." },
    { "id": "s8", "title": "八、结论与建议", "content": "..." }
  ]
}

## 写作准则
- 语言专业、客观、数据驱动
- 不编造数字，只说"约XX"时需基于提供的数据
- 每段200-400字，有实质分析
- 用中文

## 8段内容指引
1. 公司概况：主营业务、商业模式、竞争优势、市场地位
2. 财务分析：营收/利润趋势，重点分析最新数据
3. 技术分析：股价走势、52周高低、技术形态
4. 市场情绪：机构关注度、资金流向
5. 竞品对比：与2-3家可比公司对比
6. 估值与健康度：PE/PB、负债率、分红
7. 关键风险：3-5个具体的风险因素
8. 结论与建议：短期(0-6月)和长期(6-18月)观点`;
}

export function parseJSON(text) {
  // Try raw parse
  try { return JSON.parse(text); } catch {}

  // Try extracting from code fences (json or plain)
  let m = text.match(/```(?:json)?\s*\n?([\s\S]*?)```/);
  if (m) try { return JSON.parse(m[1].trim()); } catch {}

  // Try finding first { and last }
  const start = text.indexOf('{');
  const end = text.lastIndexOf('}');
  if (start !== -1 && end > start) {
    try { return JSON.parse(text.slice(start, end + 1)); } catch {}
  }

  // Last resort: show the first 500 chars of response
  throw new Error(`Could not parse JSON. Response starts: ${text.slice(0, 500)}`);
}

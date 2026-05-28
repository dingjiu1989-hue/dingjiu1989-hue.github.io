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
  "subtitle": "一句话副标题，10-20字，类似「AI算力霸主的芯片帝国」「高股息银行股的估值修复之路」，提炼公司核心投资逻辑",
  "executive_summary": "三段核心摘要（每段含核心**数字**），每段2-3句，用\\n\\n分隔",
  "sections": [
    { "id": "s1", "title": "一、公司概况", "content": "使用 Markdown 格式的200-500字分析" },
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

### 子标题
用 ### 做内容分层，例如：### 2.1 营收趋势\n### 2.2 盈利能力

### 加粗
所有关键数字用 **数字+单位** 包裹，如**营收1788亿元**、**净利润610亿元**、**毛利率34%**

### 列表
- 用 - item 枚举业务板块、竞争优势、数据要点
- 每个要点20-40字，包含具体数值
- 至少使用1-2个列表

### 编号列表
1. 用 1. 2. 3. 列举风险因素
2. 每个风险包含机制描述和影响程度

### 表格（特别重要）
竞品对比章（s5）和估值章（s6）必须各含至少一个对比表格：
| 指标 | 谷歌 | 公司A | 公司B |
|------|------|-------|-------|
| 营收 | **XX** | **XX** | **XX** |
对比表格放在章节末尾。

### 段落
- 段落之间空行分隔
- 段落开头用文字，中间嵌入 **加粗数字**
- 避免纯段落超过4行

## 写作准则
- 语言专业、客观、数据驱动
- 不编造数字，引用的数据必须来自用户提供的输入
- **禁止输出"数据缺失"、"暂缺"、"未提供"等弱化语气**——直接跳过无数据内容
- 每章节200-500字，有实质分析
- 用中文
- 行之间用换行符\\n分隔

## 8段内容指引
1. **公司概况**：用列表写3-4个业务板块；用编号写2-3个竞争壁垒（客户锁定、规模效应、技术领先）
2. **财务分析**：用###分营收趋势、盈利能力、资产质量三个子节；每个子节用列表枚举关键**数字**
3. **技术分析**：用列表写价格位置（52周最高/**X**、最低/**Y**、当前/**Z**）；技术指标用列表（RSI、MACD、均线）；成交量和趋势分析用段落
4. **市场情绪**：用段落分布研报评级；用列表写资金流向数据
5. **竞品对比**：前2/3用段落分析，后1/3必须加对比表格（| 指标 | 公司A | 公司B | 公司C |...|）
6. **估值与健康度**：用列表写PE/PB/PEG估值水平；用段落分析财务健康度（负债率、流动比率）；末尾加健康度评分表
7. **主要风险**：必须用1. 2. 3. 4. 5. 编号列表，每项含风险描述+影响路径
8. **结论与建议**：短评用段落；短期（0-6月）和长期（6-18月）用列表写目标价和逻辑`;
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

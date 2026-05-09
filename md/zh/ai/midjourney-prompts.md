---
title: "Midjourney 提示词大全：从入门到进阶"
description: "系统整理 Midjourney 提示词结构、参数体系与风格参考，附赠 10 套实战验证的提示词模板，涵盖写实人像、Logo 设计、产品摄影等高频场景。"
date: 2026-05-09
board: ai
url: https://dingjiu1989-hue.github.io/ai/midjourney-prompts.html
---

# Midjourney 提示词大全：从入门到进阶

Midjourney 凭借其出色的美学质量和极低的使用门槛，已经成为 AI 绘画领域用户最多的平台。但很多人使用 MJ 的方式是"随缘出图"——同样的提示词在不同版本下效果天差地别，或者始终无法复现别人的惊艳效果。本文从提示词结构到参数体系，再到 10 套可以直接复用的提示词模板，帮你系统掌握 Midjourney。

## 提示词的基本结构

一条完整的 Midjourney 提示词由以下元素组成，建议按照这个顺序排列：
    
    
    [主体] + [媒介/风格] + [环境] + [光线] + [色彩] + [情绪] + [构图] --参数1 值1 --参数2 值2

举例说明：
    
    
    a samurai warrior with a glowing katana, digital painting, misty mountain peak at dawn,
    volumetric lighting, amber and indigo color palette, epic and melancholic mood,
    low angle shot, dynamic pose --ar 16:9 --v 6.1 --s 300

注意，Midjourney 对自然语言的理解能力远强于 Stable Diffusion，你可以使用完整的英语句子而不用担心模型"听不懂"。

## V6 vs V7：你需要知道的差异

Midjourney V6（2024 年初发布）和 V7（2026 年初发布）之间的差异非常大：

  * **V6 的特点：** 对提示词的忠实度更高，更擅长理解长提示词和复杂描述。但有时过于死板，缺乏"意外惊喜"。
  * **V7 的特点：** 引入"个人化"（Personalization）功能，能根据你的历史偏好调整输出。美学质量更高，但在某些场景下对提示词的响应不如 V6 精确。
  * **兼容性：** V7 后 --v 6.1 依然可用。如果你的工作流依赖特定风格的批次一致性，建议继续使用 V6.1。如果追求新用户界面和个性化体验，选 V7。



## 关键参数速查表

参数 | 语法 | 作用 | 建议值  
---|---|---|---  
**画面比例** | \--ar 宽:高 | 控制输出尺寸 | 人像 3:4，风景 16:9，方形 1:1  
**风格化** | \--s 0-1000 | 值越高 AI 自由度越大，画面越艺术化 | 写实 50-100，艺术 250-500，抽象 600+  
**怪异度** | \--w 0-3000 | 控制输出内容的离奇程度 | 日常使用 0-500，创意探索 1000+  
**版本** | \--v 版本号 | 指定模型版本 | 推荐 6.1 或 7  
**风格参考** | \--sref URL | 用另一张图的风格生成新图 | 配合 --sw 0-1000 控制参考强度  
**角色参考** | \--cref URL | 保持同一人物的面部特征 | 配合 --cw 0-100 控制参考权重  
  
## \--sref 和 --cref：风格与角色参考

这两个是 Midjourney 最强大的功能之一。**\--sref** （Style Reference）让你指定一张参考图，MJ 会提取其色彩、光影和纹理风格，应用到新生成的图片上。**\--cref** （Character Reference）则是保持角色一致性的关键工具——你想让同一个角色的脸出现在不同场景中，给一个 --cref 链接就行。

实际使用中，--cref 有时会"翻车"（生成相似但不完全一致的脸），这时可以结合 **\--cw 50** 把权重降到中间值，在保留面部特征的同时给 AI 更多创作空间。对于 --sref，推荐的做法是选 3-4 张风格接近的参考图，用空格分隔多个 URL，MJ 会自动融合。

## 10 套实战提示词模板

以下模板经过大量测试验证，直接替换方括号中的内容即可使用。

  1. **写实人像：**  
`portrait of [age] [gender] with [distinctive feature], [facial expression], natural window lighting, shot on 85mm lens, f/1.8, shallow depth of field, realistic skin texture, high fidelity --ar 3:4 --s 50 --v 6.1`
  2. **产品摄影：**  
`[product name] on a minimalist white table, soft studio lighting, commercial product photography, clean background, high detail, 8k --ar 4:3 --s 100 --v 6.1`
  3. **电影级风景：**  
`cinematic landscape of [location], [time of day], dramatic sky, volumetric clouds, golden hour lighting, epic wide shot, shot on IMAX camera --ar 16:9 --s 250 --v 6.1`
  4. **Logo 设计：**  
`minimalist logo for [brand], flat vector style, [primary color] and [secondary color], geometric shapes, clean lines, white background --ar 1:1 --s 50 --v 6.1`
  5. **UI 界面线框图：**  
`mobile app ui wireframe for [app type], grayscale, minimalist design, ios design system, clear layout, high contrast --ar 9:16 --s 0 --v 6.1`
  6. **概念艺术 / 角色设计：**  
`character design of a [occupation/race] in a [genre] world, full body concept art, turn around sheet, defined by [style reference], game art --ar 3:4 --s 400 --v 6.1`
  7. **建筑室内设计：**  
`interior of a [room type] with [style] decor, natural light from [direction], wide angle lens, architectural photography, realistic textures --ar 4:3 --s 150 --v 6.1`
  8. **像素艺术：**  
`pixel art of [scene], 16-bit style, retro game aesthetic, limited color palette, blocky details --ar 16:9 --s 100 --v 6.1`
  9. **3D 渲染 / 盲盒风格：**  
`3D render of a cute [cute character], blind box toy style, soft studio lighting, pastel colors, bokeh background, C4D render, octane render --ar 1:1 --s 200 --v 6.1`
  10. **国风 / 水墨画：**  
`[subject] in classical Chinese ink wash painting style, brush strokes, misty atmosphere, traditional scroll composition, black ink and subtle color, zen mood --ar 3:4 --s 300 --v 6.1`



每个模板中的核心变量都标注了方括号。建议先原样跑一次确认效果，再逐步替换变量。注意，V6.1 下效果最稳定——V7 的风格化逻辑不同，部分模板需要微调 --s 值。

## 写在最后

Midjourney 的进化速度非常快，每两到三个月就有重大更新。保持学习的最好方式不是背诵参数，而是理解每个参数背后的原理——它控制的是 AI 的"自由度"还是"约束力"。掌握了这个底层逻辑，任何版本更新你都能快速上手。

### 📖 相关推荐

  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/ai/ai-art-monetization.html>)
  * [Stable Diffusion 出图入门指南](<https://dingjiu1989-hue.github.io/ai/stable-diffusion.html>)
  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/ai/ai-coding-tools-comparison-2026.html>)



**See also:** [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](</ai/ai-coding-tools-comparison-2026.html>), [MCP 协议入门：让 AI 模型安全访问你的工具和数据](</ai/mcp-protocol-guide.html>), [AI Agent 开发入门 2026：从原理到第一个智能体](</ai/ai-agent-development-2026.html>).

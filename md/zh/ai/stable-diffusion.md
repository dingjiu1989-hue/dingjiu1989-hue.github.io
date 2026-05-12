---
title: "Stable Diffusion 出图入门指南"
description: "零基础入门 Stable Diffusion，详解 Checkpoint、Sampler、Steps、CFG Scale 等核心参数，手把手教你从安装到出第一张高质量图片。"
date: 2026-05-12
board: ai
url: https://dingjiu1989-hue.github.io/zh/ai/stable-diffusion.html
---

# Stable Diffusion 出图入门指南

AI 绘画领域三足鼎立：Midjourney 以品质著称，DALL-E 3 以理解力见长，而 Stable Diffusion 则以其免费、开源、高度可定制性成为技术用户的首选。本文面向零基础用户，带你从安装到参数调优，完整走通 Stable Diffusion 的出图流程。 三大工具的定位差异 在开始之前，有必要先理解 Stable Diffusion 和其他工具的定位区别：

  * **Midjourney** ——闭源、付费、零门槛。你不需要理解任何技术参数，输入一句话就能得到赏心悦目的图片。代价是你几乎没有控制权，风格局限在 Midjourney 的审美体系内。
  * **DALL-E 3** ——以语义理解能力著称。你说"A 在 B 的左边，C 在 A 的上面"，它真的能准确布局。但对艺术风格的控制力远不如 SD。
  * **Stable Diffusion** ——开源、免费、完全可控。你可以选择任意模型（Checkpoint）、调整每个参数、在本地运行、甚至可以训练自己的 LoRA。代价是学习曲线陡峭。

从安装到第一次出图 Stable Diffusion 最流行的启动器是 **Automatic1111 WebUI** （适合新手）和 **ComfyUI** （适合追求工作流复用的用户）。建议新手从 Automatic1111 开始。 安装后，你至少要准备一个 Checkpoint 模型（也就是"主模型"）。初学者推荐 **DreamShaper** 或 **Realistic Vision** ——前者适合艺术风格，后者追求写实感。从 Hugging Face 或 CivitAI 下载 .safetensors 文件，放入 models/Stable-diffusion/ 目录即可。 准备工作完成后，最基本的出图流程是：输入提示词 → 选择 Checkpoint → 点击 Generate。但如果你想让图片质量可控，就必须要理解下面这些参数。 核心参数详解 参数 | 作用 | 推荐值 | 过高/过低的表现  
---|---|---|---  
**Sampler（采样器）** | 控制去噪算法 | Euler a / DPM++ 2M Karras | Euler a 速度快但风格偏软；DPM++ 细节更丰富但慢 30%  
**Steps（步数）** | 采样的迭代次数 | 20-30 | 低于 15 步画面粗糙；高于 50 步边际收益消失，偶尔引入噪点  
**CFG Scale** | 提示词跟随强度 | 7-9 | 低于 4 画面与提示词无关；高于 15 色彩过饱和、细节变形  
**Resolution** | 输出图片分辨率 | 512x512 / 768x768 | 超过 1024 可能导致人物崩坏；需配合高分辨率修复（Hires.fix）  
**Seed（种子）** | 随机数种子 | -1 (随机) | 固定种子可复现结果，微调提示词时使用相同种子来对比效果  
提示词结构：高质量出图的基础 Stable Diffusion 的提示词遵循一个经典的四段式结构：

    最佳画质, 主体描述, 环境/背景, 风格/艺术家参考, 技术参数

一个实际例子：

    positive prompt:
    masterpiece, best quality, (1girl:1.2), solo, detailed face,
    beautiful detailed eyes, (flower crown:1.1), soft lighting,
    cherry blossoms in background, spring atmosphere,
    art by wlop and akihiko yoshida,
    highres, 8k, cinematic lighting, depth of field

    negative prompt:
    worst quality, low quality, ugly, deformed, blurry,
    bad anatomy, bad hands, extra fingers, missing fingers,
    monochrome, watermark, text, signature, nsfw

括号语法 `(keyword:weight)` 用于调整某个词的重要程度，权重默认 1.0，范围通常 0.5-1.5。多个关键词用逗号分隔，**越靠前的词权重越高** 。 负面提示词（Negative Prompt）是 SD 区别于 Midjourney 的重要特性。你告诉 AI 不要生成什么，它就会刻意避免。常见负面词包括：低质量、畸形肢体、多余手指、水印文字等。 实战调参演示 假设我们要生成一张"一个女孩在樱花树下看书"的图片： **第一次尝试（默认参数，简单提示词）：**  
提示词：a girl reading under cherry tree  
CFG 7, Steps 20, Euler a, 512x512  
结果：人物模糊，手部变形，背景只有模糊的粉色色块。 **优化后（结构化提示词 + 负向 + 参数调整）：**  
提示词：masterpiece, best quality, 1girl, reading a book, sitting under cherry blossom tree, detailed kimono, soft afternoon light, petals falling, cinematic angle  
负面提示词：worst quality, bad hands, extra fingers, blurry  
Checkpoint: DreamShaper, CFG 7, Steps 25, DPM++ 2M Karras, 768x768  
结果：人物面部清晰，手部基本正常，整体构图有了氛围感。 差距出在哪？第一是 Checkpoint 的选择——基础模型对特定风格的支持远不如社区微调模型。第二是提示词的颗粒度——"樱花树下"太模糊，"petals falling, soft afternoon light"给了 AI 可执行的视觉指令。第三是负面提示词排除了最常见的劣质输出模式。 进阶建议 当你掌握了基础出图后，可以按这个顺序进阶：先学 LoRA 模型（给特定角色或风格做微调），再学 ControlNet （用姿态图、深度图控制构图），最后学 Inpainting （局部重绘修复细节）。每一步都能显著提升你的出图质量，但前提是基础参数已经掌握扎实。 📖 相关推荐

  * [AI 绘画变现指南：从出图到接单的完整路径](<https://dingjiu1989-hue.github.io/zh/ai/ai-art-monetization.html>)
  * [Midjourney 提示词大全：从入门到进阶](<https://dingjiu1989-hue.github.io/zh/ai/midjourney-prompts.html>)
  * [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](<https://dingjiu1989-hue.github.io/zh/ai/ai-coding-tools-comparison-2026.html>)

**See also:** [AI 编程助手对比 2026：Cursor vs Copilot vs Claude Code 怎么选](</zh/ai/ai-coding-tools-comparison-2026.html>), [MCP 协议入门：让 AI 模型安全访问你的工具和数据](</zh/ai/mcp-protocol-guide.html>), [AI Agent 开发入门 2026：从原理到第一个智能体](</zh/ai/ai-agent-development-2026.html>).

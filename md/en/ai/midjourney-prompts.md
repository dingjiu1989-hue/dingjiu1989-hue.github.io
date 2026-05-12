---
title: "Midjourney Prompt Guide: From Basics to Pro-Level Images"
description: "Master Midjourney prompt structure, parameters, and style references. Includes 10 battle-tested prompt templates for portraits, logos, product shots, and more."
date: 2026-05-03
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/midjourney-prompts.html
---

# Midjourney Prompt Guide: From Basics to Pro-Level Images

Midjourney v7 produces stunning images, but only if you speak its language. This guide covers the prompt structure that consistently produces professional results, plus battle-tested templates you can copy and adapt.

## Prompt Structure

A well-formed Midjourney prompt has four parts:

    [Subject] + [Style/Medium] + [Lighting/Composition] + [Parameters]

    Example:
    Portrait of a female cyberpunk character, digital art style by
    WLOP and Artgerm, neon lighting with rim light from the side,
    cinematic composition --ar 2:3 --stylize 250 --v 7

## The Parameters That Matter

Parameter| What It Does| Recommendation  
---|---|---  
`--ar <w>:<h>`| Aspect ratio| 2:3 for portraits, 16:9 for landscapes, 1:1 for social media  
`--stylize <0-1000>`| Artistic flair vs prompt accuracy| 100-250 for realistic, 500-750 for artistic  
`--chaos <0-100>`| Variation between the 4 images| 0 for consistency, 30-50 for exploration, 80+ for wild ideas  
`--weird <0-3000>`| Unconventional/experimental results| 0 for normal, 500+ for creative/abstract  
`--no <element>`| Negative prompt| `--no text, watermark, signature, blurry`  

## 10 Battle-Tested Prompt Templates

### 1\. Professional Portrait

    Portrait of a [age] [gender] [profession], [setting], soft natural
    lighting, shot on 85mm f/1.4, shallow depth of field, professional
    headshot style --ar 2:3 --stylize 150

### 2\. Product Photography

    [Product] on a [color] backdrop, product photography style, studio
    lighting with soft shadows, clean and minimal, shot with macro lens,
    commercial photography --ar 1:1 --stylize 100

### 3\. Logo Design

    Minimalist logo for [company/type], vector style, flat design,
    [specific symbols/elements], [color palette], white background,
    suitable for app icon --ar 1:1 --stylize 50

### 4\. Architectural Visualization

    [Building type] architecture, [style] design, golden hour lighting,
    photorealistic 3D render, wide-angle lens, surrounded by [environment],
    architectural photography --ar 16:9 --stylize 200

### 5\. Food Photography

    [Dish name], overhead flat lay, natural window lighting, styled with
    [props/herbs], shallow depth of field, food photography, appetizing,
    vibrant colors --ar 4:5 --stylize 100

### 6\. Fantasy Landscape

    Epic fantasy landscape, [specific features], concept art by [artist
    reference], atmospheric lighting with god rays, cinematic composition,
    8K ultra detailed --ar 16:9 --stylize 500

### 7\. UI/UX Mockup

    [App type] mobile app design, clean UI, modern minimal interface,
    [color scheme], glassmorphism style, Dribbble featured, dark mode,
    figma design --ar 9:16 --stylize 80

### 8\. Character Design

    [Character description], character design sheet, multiple views
    (front, side, back), [art style], clean linework, flat colors,
    concept art, turnaround reference --ar 16:9 --stylize 200

### 9\. Isometric Illustration

    Isometric illustration of a [scene/room/building], [color palette],
    clean vector style, 3D isometric view, detailed interior, pastel
    colors, soft shadows, illustration --ar 1:1 --stylize 150

### 10\. Cinematic Scene

    [Scene description], cinematic shot, [lighting description], movie
    still from [reference director/film], anamorphic lens, film grain,
    color graded --ar 21:9 --stylize 300

## Pro Tips

  * **Use artist references sparingly.** One or two references sharpen the style. Three or more create visual chaos.
  * **Describe what you want, not what you don't want.** Use `--no` for 1-2 things max. Focus on positive description.
  * **Vary one thing at a time.** When experimenting, change one parameter at a time so you know what caused the difference.
  * **Save your best prompts.** Good prompts are assets. Build a personal library organized by category.

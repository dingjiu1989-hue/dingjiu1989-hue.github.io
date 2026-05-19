#!/usr/bin/env python3
"""Daily AI News Roundup Generator.

Usage:
  python3 scripts/gen_daily_news.py

Creates EN + CN markdown files for today's AI news roundup.
After editing the generated files with actual news content, run:
  python3 scripts/gen_en_site.py && python3 scripts/gen_ai_friendly.py
  python3 scripts/add_en_seo.py && python3 scripts/gen_rss.py
  python3 scripts/generate_json_feed.py
"""

import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()
SLUG = f"ai-daily-news-{TODAY}"

# ── English Template ──
EN_MD = f"""---
title: "AI Daily Digest — {TODAY}: [Top 3 Headlines Here]"
description: "Top 10 AI news today: [key topics]. Curated from trusted sources with full attribution."
date: {TODAY}
board: ai
url: https://dingjiu1989-hue.github.io/en/ai/{SLUG}.html
---

# AI Daily Digest — {TODAY}

## 1. [Headline 1]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 2. [Headline 2]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 3. [Headline 3]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 4. [Headline 4]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 5. [Headline 5]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 6. [Headline 6]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 7. [Headline 7]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 8. [Headline 8]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 9. [Headline 9]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

## 10. [Headline 10]

[2-3 sentence summary with key facts and context.]

**Source:** [Publication Name](https://source-url.com/article)

---

*AI Daily Digest is compiled from trusted technology news sources. For corrections or suggestions, contact us at the project repository.*
"""

# ── Chinese Template ──
CN_MD = f"""---
title: "AI每日资讯 — {TODAY}：[Top 3 Headlines in Chinese]"
description: "今日AI十大要闻：[key topics in Chinese]。附原文来源链接。"
date: {TODAY}
board: ai
url: https://dingjiu1989-hue.github.io/ai/{SLUG}.html
---

# AI每日资讯 — {TODAY}

## 1. [标题1]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 2. [标题2]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 3. [标题3]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 4. [标题4]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 5. [标题5]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 6. [标题6]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 7. [标题7]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 8. [标题8]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 9. [标题9]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

## 10. [标题10]

[2-3句中文摘要，包含关键事实和背景。]

**来源：** [媒体名称](https://source-url.com/article)

---

*AI每日资讯由编辑团队从可信科技新闻源整理。如有更正或建议，请通过项目仓库联系我们。*
"""

# ── News Sources Reference ──
SOURCES = """
Recommended AI News Sources:
  1. TechCrunch AI      — https://techcrunch.com/category/artificial-intelligence/
  2. AI News             — https://www.artificialintelligence-news.com/
  3. Maginative          — https://www.maginative.com/
  4. The Verge AI        — https://www.theverge.com/ai-artificial-intelligence
  5. Ars Technica AI     — https://arstechnica.com/ai/
  6. VentureBeat AI      — https://venturebeat.com/category/ai/
  7. ZDNet AI            — https://www.zdnet.com/topic/artificial-intelligence/
  8. MIT Tech Review AI  — https://www.technologyreview.com/topic/artificial-intelligence/
  9. TheSequence         — https://thesequence.substack.com/
  10. MarkTechPost       — https://www.marktechpost.com/
  11. 机器之心 (CN)       — https://www.jiqizhixin.com/
  12. 量子位 (CN)         — https://www.qbitai.com/
"""


def main():
    en_md_dir = ROOT / "md" / "en" / "ai"
    cn_md_dir = ROOT / "md" / "zh" / "ai"
    en_md_dir.mkdir(parents=True, exist_ok=True)
    cn_md_dir.mkdir(parents=True, exist_ok=True)

    en_path = en_md_dir / f"{SLUG}.md"
    cn_path = cn_md_dir / f"{SLUG}.md"

    if en_path.exists() or cn_path.exists():
        print(f"Daily news for {TODAY} already exists. Skipping template generation.")
        print(f"  EN: {en_path}")
        print(f"  CN: {cn_path}")
        return

    en_path.write_text(EN_MD, encoding="utf-8")
    cn_path.write_text(CN_MD, encoding="utf-8")
    print(f"Daily news templates created for {TODAY}:")
    print(f"  EN: {en_path}")
    print(f"  CN: {cn_path}")
    print()
    print("Next steps:")
    print("  1. Fill in the top 10 AI news items in both files")
    print("  2. Run: python3 scripts/gen_en_site.py")
    print("  3. Run: python3 scripts/gen_ai_friendly.py")
    print("  4. Regenerate sitemap + feeds")
    print("  5. Commit and push")
    print()
    print(SOURCES)


if __name__ == "__main__":
    main()

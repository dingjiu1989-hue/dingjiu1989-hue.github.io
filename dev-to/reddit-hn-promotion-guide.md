# Reddit & Hacker News 推广文案

## 使用说明
Each post has a recommended community, title, and body.
Post on weekdays 9-11am US Eastern for best results.
Don't post all at once — spread across 2-3 weeks.

---

## Post 1: HN Show HN — SaaS Bootstrapping Guide

**Community:** Hacker News (news.ycombinator.com)
**Type:** Show HN
**Title:** Show HN: Bootstrapping a SaaS — A Complete Roadmap from Idea to First Paying Customer

**Body:**
I compiled everything I learned bootstrapping SaaS products into a single guide. Covers: finding the right idea, validating before building, MVP tech stack recommendations, launch strategy, and pricing tiers that work for solo founders.

Happy to answer questions about any phase here. The biggest lesson: your MVP should feel embarrassingly simple. If you're not slightly uncomfortable with how minimal it is, you've built too much.

https://dingjiu1989-hue.github.io/en/sidehustle/saas-bootstrapping-guide.html

---

## Post 2: r/SideProject — Developer Side Hustles

**Subreddit:** r/SideProject (230K members)
**Title:** Compiled 10 developer side hustles ranked by effort vs earning potential

**Body:**
Went through and ranked every dev side hustle I've tried (or seen work for others). The rankings:
1. Freelancing — fastest cash, but trading time for money
2. SaaS — highest ceiling but takes 12-18 months
3. Digital products — best value/time ratio
4. APIs — underrated passive income
...and 6 more with real examples and revenue numbers.

Main takeaway: pick one and ship in 2 weeks. Analysis paralysis is the actual problem.

https://dingjiu1989-hue.github.io/en/sidehustle/developer-side-hustles-2026.html

---

## Post 3: r/SaaS — Bootstrapping Guide

**Subreddit:** r/SaaS (180K members)
**Title:** Bootstrapping a SaaS: complete 5-phase roadmap (what I wish I knew 3 years ago)

**Body:**
Phase 1: Find a problem YOU have (not one you think exists)
Phase 2: Validate with a landing page and 50 email signups before writing a line of code
Phase 3: Build the MVP — stack recommendations for solo founders in 2026
Phase 4: Launch on Product Hunt, HN, and niche communities
Phase 5: Pricing — $15-49/mo sweet spot, annual discount reduces churn

Biggest mistake I see: people build for 6 months without showing anyone. Get to "embarrassingly simple MVP" in 6 weeks max.

https://dingjiu1989-hue.github.io/en/sidehustle/saas-bootstrapping-guide.html

---

## Post 4: r/programming — Git Cheatsheet

**Subreddit:** r/programming (6M members)
**Title:** Every Git command I use in daily work — organized by what you're actually trying to do

**Body:**
Made a Git reference organized by task (not alphabetically). Sections: setup, staging, branching, undoing things, remotes, log, and interactive rebase. Includes a "what to do when things go wrong" section at the bottom — git stash, git reflog, git bisect.

The undo section alone has saved me at least 50 hours of panic over the years.

https://dingjiu1989-hue.github.io/en/tech/git-cheatsheet.html

---

## Post 5: r/ClaudeAI or r/ChatGPT — Claude vs ChatGPT

**Subreddit:** r/ClaudeAI (85K) or r/ChatGPT (6M)
**Title:** Honest Claude vs ChatGPT comparison after 6 months of using both daily

**Body:**
Not a fanboy post — just an honest breakdown by task type:

Coding: Tie. Claude for large codebases, ChatGPT for data-heavy coding.
Writing: Claude wins by a clear margin.
Long documents: Claude (200K context is a superpower).
Data analysis: ChatGPT (Code Interpreter).
Images: ChatGPT (Claude can't generate).
Web search: ChatGPT (Claude doesn't have it).

Bottom line: use both. Claude Free + ChatGPT Free = best of both worlds for $0.

https://dingjiu1989-hue.github.io/en/ai/claude-vs-chatgpt.html

---

## Post 6: r/webdev — REST API Best Practices

**Subreddit:** r/webdev (2.3M members)
**Title:** REST API best practices that actually matter in production

**Body:**
Not theoretical CS stuff — the things that bite you 6 months later:

1. Version your API from day one (URL prefix is fine)
2. Use nouns not verbs for resources
3. Consistent error response format — include a requestId
4. Right HTTP codes: 429 with Retry-After, 409 for conflicts, 422 for semantic errors
5. Cursor-based pagination for anything with >1000 records
6. OpenAPI 3.1 spec — if you don't have one, your API isn't production-ready

What did I miss? Keen to hear what conventions other teams swear by.

https://dingjiu1989-hue.github.io/en/tech/rest-api-best-practices.html

---

## Posting Schedule

| Week | Day | Platform | Article |
|------|-----|----------|---------|
| 1 | Tue 9am ET | r/SideProject | Developer Side Hustles |
| 1 | Wed 10am ET | r/programming | Git Cheatsheet |
| 1 | Thu 9am ET | Dev.to | 6 articles (post 2/day) |
| 2 | Tue 9am ET | r/SaaS | SaaS Bootstrapping |
| 2 | Wed 10am ET | HN Show HN | SaaS Bootstrapping |
| 2 | Thu 9am ET | r/webdev | REST API Best Practices |
| 3 | Tue 9am ET | r/ClaudeAI | Claude vs ChatGPT |

---

## Dev.to 发布步骤

1. 打开 https://dev.to/new
2. 打开 `/dev-to/` 下的 `.md` 文件
3. 内容粘贴到 Dev.to 编辑器
4. 确认 canonical_url 的 🔗 图标亮起（表示 canonical 生效）
5. 添加标签，封面图选 "保持原样"
6. Publish

关键：Dev.to 的 canonical URL 功能意味着这篇文章的 SEO 权重会传递给你的原文。Google 不会惩罚重复内容。

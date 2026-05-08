---
title: "Prompt Engineering: From Beginner to Expert — What Actually Works"
published: true
description: "Master the 5 elements of a good prompt: role, task, context, format, and constraints. Real before/after comparisons reveal what makes prompts work."
tags: ai, chatgpt, beginners, productivity, promptengineering
canonical_url: https://dingjiu1989-hue.github.io/en/ai/prompt-engineering.html
---

Prompt engineering isn't about memorizing magic phrases — it's about clearly communicating what you want, how you want it, and what context the AI needs.

## The Five Elements of a Good Prompt

Every effective prompt has some combination of these:

1. **Role** — Who is the AI? "You are a senior software engineer reviewing code for security vulnerabilities."
2. **Task** — What exactly should it do? "Find SQL injection vulnerabilities in the following code."
3. **Context** — What background matters? "This runs in a Node.js/Express backend with PostgreSQL."
4. **Format** — How should the output look? "List each vulnerability with location, severity, and fix."
5. **Constraints** — "Only flag HIGH or CRITICAL severity. Ignore style concerns."

## Before/After: Same Request, Different Results

**Bad Prompt:**
> Write a blog post about Docker.

*Result:* Generic 200-word overview. Useless.

**Good Prompt:**
> You are a senior DevOps engineer writing for junior developers who have never used containers. Write "Docker in 30 Minutes: From Zero to First Container." Use a friendly, conversational tone. Structure: (1) What problem Docker solves, (2) Installation, (3) Core concepts with analogies, (4) Hands-on walkthrough, (5) Common gotchas. Keep under 800 words.

*Result:* A focused, practical tutorial the audience would actually find useful.

## Key Techniques

### 1. Chain of Thought
Ask the model to think step by step before answering. This dramatically improves accuracy on reasoning tasks.

### 2. Few-Shot Prompting
Show 2-3 examples of exactly what you want. The most efficient way to communicate format and style.

### 3. Iterative Refinement
Your first prompt rarely produces a perfect result. Treat it like briefing a junior: start broad, add constraints, refine output.

## Common Mistakes
- **Being too vague** — be specific about topic, audience, format, and tone
- **Asking for too much at once** — a 5,000-word article will be shallow. Ask for one section at a time
- **Not providing examples** — when format matters, show 1-2 examples
- **Accepting the first answer** — push back and iterate

---

*Originally published at [AI Study Room](https://dingjiu1989-hue.github.io/en/ai/prompt-engineering.html) — 70+ curated articles for developers.*

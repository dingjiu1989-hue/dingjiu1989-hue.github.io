---
title: "Code Review Best Practices: How to Give and Receive Feedback That Actually Improves Code"
description: "Learn how to give useful code review feedback, write better PRs, and build a healthy review culture. Specific techniques for reviewers and authors."
date: 2025-11-27
board: tech
url: https://aidev.fit/en/tech/code-review-best-practices.html
---

# Code Review Best Practices: How to Give and Receive Feedback That Actually Improves Code

Code review is the single highest-leverage practice for shipping reliable software. Done well, it catches bugs before production, spreads knowledge across the team, and improves the codebase over time. Done poorly, it's a bottleneck that breeds resentment. Here's how to do it right.

## For Reviewers: How to Give Useful Feedback

### 1\. Review the Right Things First

Start with **correctness and security** — does the code do what it claims? Are there edge cases? Could an attacker exploit this? Then move to **design and architecture** — does this change fit the system's patterns? Will it scale? Finally, check **style and readability** — naming, comments, tests. Style nitpicks should never block a PR; use automated formatters (Prettier, Biome, Black) and linters to handle that automatically.

### 2\. Be Specific, Not Judgmental

Bad: "This is confusing." Good: "I had to read this three times to understand the intent. Could we extract the filter logic into a named function?" Bad: "Why didn't you use X pattern?" Good: "Have you considered using the repository pattern here? It would make testing this without a database easier. Here's an example from module Y."

### 3\. Distinguish Blocking from Non-Blocking

Not every comment needs to be resolved before merge. Use prefixes to make intent clear: `blocking:` for correctness/security issues that must be fixed; `suggestion:` for improvements that are worth considering but not required; `nit:` for minor style preferences; `question:` for understanding the author's intent. This small habit reduces friction dramatically.

### 4\. Review in Timeboxed Batches

Aim for reviews within 4 business hours (same-day). Review 2-3 PRs in a focused 30-minute block rather than context-switching all day. Research from Google shows that reviewers who batch reviews catch 40% more defects than those who review ad-hoc between meetings. If a PR is too large (>400 lines), ask the author to split it before reviewing.

### 5\. Lead with Praise

If something is clever, elegant, or well-tested, say so. Positive feedback reinforces good practices and makes critical feedback easier to receive. "This edge case handling is great — I would have missed the timeout scenario. The test coverage here is excellent."

## For Authors: How to Get Better Reviews

### 1\. Make Your PR Easy to Review

Keep PRs small — ideally under 400 lines. Write a clear description: what problem does this solve, what approach did you choose and why, how did you test it, and are there any risks or follow-ups? Link the issue/ticket. Add screenshots or screen recordings for UI changes.
    
    
    ## What
    Adds rate limiting middleware for the API Gateway.
    Uses token bucket algorithm per API key.
    
    ## Why
    We hit production last week when a misconfigured
    client sent 15K req/min. This prevents that.
    
    ## Testing
    - Unit tests for bucket refill and exhaustion
    - Integration test with Redis backend
    - Load test: 10K concurrent keys, p99 < 2ms
    
    ## Risks
    - Redis dependency: if Redis is down, fail open
      (allow requests rather than blocking all traffic)

### 2\. Review Your Own Code First

Before requesting review, go through your own diff line by line. You will catch typos, leftover debugging code, missing tests, and unclear variable names before anyone else sees them. This is the single highest-return habit in code review. Use `git diff main...HEAD` or your IDE's diff view and actually read every line.

### 3\. Don't Take Feedback Personally

Your code is not you. When a reviewer suggests changes, they're trying to improve the product, not attack your competence. If you feel defensive, wait 30 minutes before responding. Ask clarifying questions: "Can you help me understand why pattern X would be better here?" This turns friction into learning.

### 4\. Respond to Every Comment

Acknowledge every review comment — even if it's a thumbs-up emoji. If you disagree, explain your reasoning with data, not emotion. "I chose the simpler approach here because this endpoint gets ~10 req/day and the complexity of caching isn't worth the 50ms savings." If the discussion needs more than 3 back-and-forth comments, hop on a quick call.

## Common Pitfalls

Anti-Pattern| Why It Hurts| Better Approach  
---|---|---  
Mega-PRs (>1K lines)| Reviewers skim, miss bugs, rubber-stamp| Stack smaller PRs on top of each other  
"LGTM" culture| Defects reach production| Require at least one meaningful comment per review  
Style nitpicks in review| Wastes human attention on automatable issues| Auto-formatter + linter in CI; humans focus on logic  
Review bottleneck (one gatekeeper)| PRs queue up, velocity drops| Distribute review load; any senior dev can approve  
Reviewing without context| Misses architectural problems| Include design doc link or 2-sentence context  
  
## Measuring Code Review Health

Track these metrics (but never use them for performance reviews — they gamify easily): **Time to first review** (target: < 4 business hours), **Time to merge** (target: < 24 hours), **PR size** (median < 300 lines), **Review depth** (comments per PR, 3+ is healthy). Tools like LinearB, CodeClimate Velocity, and GitHub's built-in insights can track these.

Great code review is a skill that compounds. Every thoughtful review makes the next one easier because the team converges on shared standards. Start with one habit from this guide — small PRs or blocking/non-blocking prefixes — and build from there.

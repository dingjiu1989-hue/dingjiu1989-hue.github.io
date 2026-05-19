---
title: "When to Refactor vs Rewrite: A Developer's Decision Framework for 2026"
description: "Practical decision framework for choosing between refactoring and rewriting. Includes strangler fig pattern, characterization tests, real-world case studies, and red flags to watch for."
date: 2025-11-28
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/refactor-vs-rewrite.html
---

# When to Refactor vs Rewrite: A Developer's Decision Framework for 2026

Every developer faces this decision eventually: the codebase is painful to work with, and you need to decide whether to refactor incrementally or rewrite from scratch. This guide gives you a decision framework, real-world data, and a step-by-step approach for either path.

## The Decision Framework

Before you choose, answer these five questions honestly:

  1. **Do you understand what the code does?** If nobody on the team fully understands the current system's behavior, a rewrite is almost guaranteed to miss critical edge cases. Rewrites of poorly-understood systems fail 80%+ of the time.
  2. **Is the technology fundamentally obsolete?** If the codebase uses a framework that's end-of-life, a language version 5 years out of support, or an architecture that can't scale to your needs — that's a legitimate reason to rewrite.
  3. **How many paying users depend on this system?** More users = more edge cases the rewrite must handle. The Netscape rewrite (1998) took 3 years and lost the browser war. The lesson: rewrites of systems with many users are extremely risky.
  4. **Can you ship incrementally?** The single biggest predictor of success is whether you can deliver value in small pieces. If you can refactor module by module while the system continues to work, do that.
  5. **Do you have test coverage?** Without tests, you can't refactor safely. If the codebase has no tests, add characterization tests first (tests that capture current behavior, correct or not) before changing anything.



## When to Refactor

Refactoring is the right choice when the codebase fundamentally works but is hard to change. Signs: the architecture is sound but the implementation is messy; you understand the domain and business rules; there are tests (or you can add them); users aren't complaining about correctness, only about slow feature delivery.

### The Strangler Fig Pattern

The safest refactoring approach: replace one piece at a time. Name comes from the strangler fig tree, which grows around a host tree and eventually replaces it entirely. In software: create a new module alongside the old one, route traffic gradually, remove the old module when nothing depends on it anymore. This works for: monolith-to-microservices, framework upgrades, database migrations, and UI rewrites.
    
    
    router.get('/users/:id', (req, res) => {
      // Gradually route to new implementation
      if (featureFlag('new-user-service', req)) {
        return newUserService.getUser(req.params.id);
      }
      return oldUserController.getUser(req.params.id);
    });

### Refactoring Tactics That Work

  * **Characterization tests first.** Write tests that capture what the code DOES, not what it SHOULD do. Then refactor. If a characterization test fails, you know you changed behavior.
  * **One refactor per PR.** Don't mix refactoring with feature changes. "I'll just clean up this file while I'm adding the feature" is how bugs are born and code reviews become impossible.
  * **Set a timebox.** Refactoring without a deadline becomes an endless project. "We'll spend 20% of each sprint on refactoring" works better than "we'll refactor until it's clean."
  * **Measure before and after.** Track: time to add a simple feature, bug rate, test run time, deploy frequency. If refactoring isn't improving these, stop.



## When to Rewrite

Rewrites are appropriate when: the technology is genuinely obsolete (COBOL on a mainframe you can't hire for, a PHP 5 codebase riddled with security holes); the architecture can't support future requirements (a single-server monolith when you need multi-region deployment); the codebase is so broken that every feature takes 5x longer than it should; and critically — the system is small enough that a rewrite can be completed in under 3 months.

### The "Rewrite Trap" to Avoid

Most rewrites fail for the same reason: the team underestimates how much implicit knowledge is embedded in the old code. The old system handles hundreds of edge cases that nobody documented. The rewrite looks cleaner but misses these cases, and users notice. Mitigation: run the old system in parallel. Route a percentage of traffic to the new system. Compare responses. Only cut over when the new system matches the old one on all critical paths for at least 2 weeks.

## Case Studies

Project| Approach| Outcome| Lesson  
---|---|---|---  
Netscape (1998)| Full rewrite| 3 years, lost market| Never stop shipping while rewriting  
GitHub (2016-2019)| Gradual refactor| Monolith → services, no downtime| Strangler fig + feature flags works  
Basecamp (2020-2021)| Incremental rewrite| Rails → Hotwire, shipped throughout| Ship every 6 weeks regardless  
Etsy (2014-2016)| Strangler fig| PHP monolith → services, continuous delivery| Route traffic before removing old code  
  
## The Practical Middle Path

Most situations call for neither pure refactor nor pure rewrite, but a combination:

  1. **Extract the most painful module first.** Identify the one part of the system that causes the most bugs or slows down development the most. Extract or rewrite just that module.
  2. **Put a clean API boundary around legacy code.** Even if you can't refactor the internals, wrapping legacy code in a clean interface lets new code interact with it safely. Eventually, replace the implementation behind the interface.
  3. **Use the "new component" rule.** All new features go into the new architecture. The old codebase becomes read-only except for critical bug fixes. Over time, the proportion of new to old code shifts.
  4. **Set a sunset date for the old system.** "We will turn off the old user service by Q3 2026." Without a deadline, the old system lives forever because "we still need that one feature."



## Red Flags That Mean Stop Whatever You're Doing

  * **Nobody can explain the current behavior.** If even senior engineers don't know what the system does in edge cases, you cannot safely rewrite it. Add monitoring and characterization tests first.
  * **The rewrite timeline is "6-12 months."** Rewrites that are estimated at 6+ months almost always take 2-3x longer. If you can't do it in 3 months, you should be refactoring instead.
  * **Users are actively using the product.** A working product with messy code is worth more than a clean codebase with no users. Don't sacrifice user value for code aesthetics.
  * **The team is split.** If half the team wants to refactor and half wants to rewrite, you have a communication problem, not a code problem. Neither approach will succeed without team alignment.



**Bottom line:** Refactoring is the default right answer in 80% of cases. Rewrites win when the technology is truly obsolete or the system is small enough to replace quickly. The worst outcome isn't messy code — it's a rewrite that takes 18 months, misses critical features, and kills the product. Ship incrementally, measure everything, and let data drive the decision.

**See also:** [Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each](</en/tech/testing-strategies-web-apps.html>), [WebAssembly Guide 2026: Running Native Code in the Browser with Rust and WASI](</en/tech/webassembly-guide.html>), [Rust vs Go: A Practical Comparison](</en/tech/rust-vs-go-practical.html>)

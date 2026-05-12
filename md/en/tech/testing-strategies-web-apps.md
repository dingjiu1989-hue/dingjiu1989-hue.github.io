---
title: "Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each"
description: "Stop guessing which tests to write. A practical guide to the testing trophy model — unit, integration, and e2e test strategies with real code examples."
date: 2026-05-08
board: tech
url: https://dingjiu1989-hue.github.io/en/tech/testing-strategies-web-apps.html
---

# Testing Strategies for Web Apps: Unit, Integration, E2E, and When to Use Each

Testing is easy to get wrong. Too many unit tests give false confidence. Too few integration tests miss real bugs. Too many E2E tests make CI slow. Here's a practical guide to the Testing Trophy — the modern testing strategy that actually works.

## The Testing Trophy (Not the Testing Pyramid)

The classic testing pyramid said "lots of unit, some integration, few E2E." The Testing Trophy inverts this: integration tests provide the most confidence per dollar, so write more of them.

| Unit Tests| Integration Tests| E2E Tests  
---|---|---|---  
**Tests**|  Single function/component| Multiple modules together| Full user flow in browser  
**Speed**|  Fastest (ms)| Fast (10-100ms)| Slow (seconds)  
**Confidence**|  Low (isolated)| High (integration is the risk)| Highest (real UX)  
**Flakiness**|  None| Low| High (network, timing)  
**Debugging**|  Easiest| Moderate| Hardest  
**Recommended ratio**|  20%| 60%| 20%  

## Unit Tests — Test Pure Logic Exhaustively

Unit tests shine for pure functions: validation logic, data transformation, utility functions, and business rules. Don't unit test React components in isolation — that's what integration tests are for. Don't test implementation details (test behavior, not methods).

    // Good unit test: pure business logic
    describe("calculateDiscount", () => {
      it("gives 20% off orders over $100", () => {
        expect(calculateDiscount({ total: 150, coupon: null })).toBe(30);
      });
      it("stacks with coupon, max 50%", () => {
        expect(calculateDiscount({ total: 100, coupon: "SAVE30" })).toBe(40);
      });
    });

## Integration Tests — The Confidence Backbone

Integration tests verify that multiple units work together. For frontend: render a component with real state, click something, assert the DOM. For backend: hit an endpoint, verify the database state. These catch the bugs unit tests miss.

    // Frontend integration test: render + interact + assert
    test("submits form and shows success", async () => {
      render(<SignupForm />);
      await user.type(screen.getByLabel("Email"), "test@example.com");
      await user.click(screen.getByText("Sign Up"));
      expect(await screen.findByText("Check your email")).toBeVisible();
    });

    // Backend integration test: request → response
    test("POST /api/users creates user in DB", async () => {
      const res = await request(app)
        .post("/api/users")
        .send({ email: "test@example.com", name: "Test" });
      expect(res.status).toBe(201);
      const user = await db.query("SELECT * FROM users WHERE email = $1", ["test@example.com"]);
      expect(user.rows[0].name).toBe("Test");
    });

## E2E Tests — Validate Critical User Flows

E2E tests drive a real browser through your most important flows: signup, login, purchase, onboarding. Keep these to critical paths only — they're slow and can be flaky. Playwright is the best E2E tool in 2026.

    // E2E: only critical paths
    test("user can complete purchase", async ({ page }) => {
      await page.goto("/products/widget");
      await page.click("text=Add to Cart");
      await page.click("text=Checkout");
      await page.fill("[name=card]", "4242424242424242");
      await page.click("text=Pay $29.00");
      await expect(page.locator(".confirmation")).toContainText("Thank you");
    });

## Testing Stack Recommendations

Layer| Tool| When  
---|---|---  
Unit| Vitest| Pure functions, utils, business logic  
Component Integration| Vitest + Testing Library| Any component with user interaction  
Backend Integration| Vitest + Supertest| API endpoints, DB writes  
E2E| Playwright| Signup, login, purchase, onboarding  
Visual Regression| Chromatic / Percy| Design system components  

**Bottom line:** Write mostly integration tests. They provide the best confidence-to-effort ratio. Unit test pure logic. E2E test only critical flows (max 20 scenarios). A slow CI pipeline is a broken one — keep E2E count low. See also: [build tools](</en/compare/vite-vs-webpack-vs-turbopack.html>) (Vitest is built on Vite) and [CI/CD tools comparison](</en/tools/best-cicd-tools-2026.html>).

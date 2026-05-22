---
title: "Error Handling Best Practices: From Try/Catch to Structured Errors"
description: "Move from random try/catch blocks to a structured error handling system. Covers error types, logging strategies, user-facing messages, and monitoring integration."
date: 2025-10-10
board: tech
url: https://aidev.fit/en/tech/error-handling-best-practices.html
---

# Error Handling Best Practices: From Try/Catch to Structured Errors

Random try/catch blocks aren't error handling — they're error hiding. A proper error handling system makes your app debuggable, observable, and resilient. Here's how to move from ad-hoc catches to a structured error system.

## Error Types — One Size Doesn't Fit All

Error Type| HTTP Status| Retry?| Show User?| Notify Dev?  
---|---|---|---|---  
**Validation error**|  400| No (fix input)| Yes (what to fix)| No  
**Not found**|  404| No| Yes (friendly message)| No  
**Authentication error**|  401| No (log in first)| Yes ("please log in")| No  
**Authorization error**|  403| No| Yes ("you don't have access")| Maybe (possible attack)  
**Rate limit**|  429| Yes (with backoff)| Yes ("too many requests")| No  
**External service failure**|  502| Yes (with backoff)| No (mask it)| Yes (oncall)  
**Internal error (unexpected)**|  500| Maybe| No (mask it)| Yes (immediately)  
  
## Structured Error Handling Pattern
    
    
    // 1. Define error hierarchy
    class AppError extends Error {
      constructor(
        message: string,
        public statusCode: number,
        public code: string,
        public retryable: boolean = false,
        public userMessage?: string
      ) {
        super(message);
        this.name = "AppError";
      }
    }
    
    class ValidationError extends AppError {
      constructor(message: string, public fields: Record<string, string>) {
        super(message, 400, "VALIDATION_ERROR", false, message);
      }
    }
    
    class ExternalServiceError extends AppError {
      constructor(service: string, cause: Error) {
        super(
          `${service} request failed`,
          502,
          "EXTERNAL_SERVICE_ERROR",
          true,
          "Something went wrong. Please try again."
        );
        this.cause = cause;
      }
    }
    
    // 2. Use in your code
    async function chargeCustomer(amount: number, token: string) {
      try {
        return await stripe.charges.create({ amount, source: token });
      } catch (error) {
        throw new ExternalServiceError("Stripe", error as Error);
      }
    }

## Global Error Handler (Express/Fastify)
    
    
    // 3. Global error handler — consistent responses
    app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
      if (err instanceof AppError) {
        return res.status(err.statusCode).json({
          error: {
            code: err.code,
            message: err.userMessage || err.message,
            fields: err instanceof ValidationError ? err.fields : undefined,
          },
        });
      }
    
      // Unexpected error — log and mask
      logger.error({ err, path: req.path, method: req.method });
      Sentry.captureException(err);
    
      return res.status(500).json({
        error: {
          code: "INTERNAL_ERROR",
          message: "An unexpected error occurred. We've been notified.",
        },
      });
    });

## Async Error Handling in Express
    
    
    // Express 4 doesn't catch async errors — use a wrapper
    const asyncHandler = (fn: Function) =>
      (req: Request, res: Response, next: NextFunction) =>
        Promise.resolve(fn(req, res, next)).catch(next);
    
    app.get("/users/:id", asyncHandler(async (req, res) => {
      const user = await db.users.findById(req.params.id);
      if (!user) throw new AppError("User not found", 404, "NOT_FOUND");
      res.json(user);
    }));
    // Express 5 (beta) handles async errors natively

## Client-Side Error Handling
    
    
    // React Error Boundary + toast
    function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
      return (
        <div role="alert">
          <h2>Something went wrong</h2>
          <pre>{error.message}</pre>
          <button onClick={resetErrorBoundary}>Try again</button>
        </div>
      );
    }
    
    // Wrap sections, not the whole app
    <ErrorBoundary FallbackComponent={ErrorFallback}>
      <CheckoutForm />
    </ErrorBoundary>

## Error Handling Checklist

  * Define error classes (not just `new Error("something went wrong")`).
  * Validate inputs at the boundary. Return 400, not 500.
  * Mask internal errors from users. Log the real error, show a generic message.
  * Add a request ID to every error log. Makes debugging across services possible.
  * Alert on 5xx spike, not every 5xx. A single 500 might be a blip. 50 in a minute is an incident.



**Bottom line:** Structured errors + global handler + external service retries + proper logging = an error system that helps you fix bugs instead of hiding them. See also: [Testing Strategies](</en/tech/testing-strategies-web-apps.html>) and [CI/CD Tools](</en/tools/best-cicd-tools-2026.html>).

**See also:** [Python asyncio Complete Guide: Coroutines, Tasks, and Event Loops](</en/tech/python-asyncio-guide.html>), [Rate Limiting Strategies for APIs: Token Bucket, Sliding Window, and Beyond](</en/tech/rate-limiting-strategies.html>), [Web Security Basics: CORS, CSP, XSS, CSRF — What Every Developer Must Know](</en/tech/web-security-basics.html>)

---
title: "Secure Code Review"
description: "A systematic approach to secure code review with checklists, automation, SAST integration, and common findings."
date: 2026-05-12
board: security
url: https://dingjiu1989-hue.github.io/en/security/secure-code-review.html
---

# Secure Code Review

Why Secure Code Review?   
Secure code review catches vulnerabilities before they reach production. It complements automated scanning by finding logic flaws and business logic vulnerabilities that tools miss.   
The Security Review Checklist   
Every code review should check these categories:   

    # secure-code-review-checklist.yaml

    authentication:

      - Are passwords hashed with bcrypt/argon2?

      - Is session management secure?

      - Are tokens properly validated?

    authorization:

      - Are access controls checked server-side?

      - Is there IDOR protection?

      - Are roles enforced at API level?

    input_validation:

      - Are all inputs sanitized?

      - Is parameterized queries used for SQL?

      - Is there XSS protection?

    cryptography:

      - Are only modern algorithms used?

      - Is key management secure?

      - Is TLS configured properly?

    error_handling:

      - Are error messages information-free?

      - Is logging sensitive data avoided?

      - Are exceptions handled gracefully?

SAST Integration   
Static Application Security Testing (SAST) automates vulnerability detection:   

    # SAST results triage

    import json

    class SASTTriage:

        def __init__(self):

            self.false_positive_patterns = [

                r"test_.*\.py",

                r"__tests__/",

                r"mock_"

            ]

        def triage_findings(self, sast_results):

            actionable = []

            false_positives = []

            for finding in sast_results:

                if any(re.match(p, finding["file"]) for p in self.false_positive_patterns):

                    false_positives.append(finding)

                    continue

                # Critical findings in production code

                if finding["severity"] == "critical" and finding["branch"] == "main":

                    actionable.insert(0, finding)  # Priority

                else:

                    actionable.append(finding)

            return actionable, false_positives

Common Findings   
SQL Injection   

    # VULNERABLE

    def get_user(username):

        query = f"SELECT * FROM users WHERE username = '{username}'"

        return db.execute(query)

    # SECURE

    def get_user(username):

        query = "SELECT * FROM users WHERE username = ?"

        return db.execute(query, (username,))

Insecure Direct Object Reference (IDOR)   

    // VULNERABLE

    app.get("/api/order/:id", (req, res) => {

      const order = db.findOrder(req.params.id);

      res.json(order);  // No ownership check!

    });

    // SECURE

    app.get("/api/order/:id", (req, res) => {

      const order = db.findOrder(req.params.id);

      if (order.userId !== req.session.userId) {

        return res.status(403).json({ error: "Forbidden" });

      }

      res.json(order);

    });

Automated Enforcement in CI   

    # .github/workflows/security-review.yml

    name: Security Review

    on: [pull_request]

    jobs:

      sast:

        runs-on: ubuntu-latest

        steps:

          - uses: actions/checkout@v4

          - name: Run SAST

            run: semgrep --config=auto --error .

          - name: Dependency scan

            run: trivy fs --severity CRITICAL,HIGH .

Manual Review Techniques   
For manual review, focus on:   

* **Data flow**: Where does untrusted data enter and exit?
2\. **Authentication bypass**: Can you reach authenticated endpoints without a valid session? 3\. **Privilege escalation**: Can a low-privilege user perform admin actions? 4\. **Race conditions**: Are there TOCTOU (time-of-check-time-of-use) issues?   
Conclusion   
Effective secure code review combines automated SAST scanning with manual review of critical code paths. Build a review checklist, integrate security into your CI pipeline, and train developers on common vulnerability patterns. The best vulnerability is the one caught before it reaches production.

---
title: "Database Audit Triggers: Automatic Change Tracking"
description: "Implement database audit logging with triggers: audit tables, trigger functions, and compliance reporting."
date: 2026-04-13
board: database
url: https://aidev.fit/en/database/database-audit-triggers.html
---

# Database Audit Triggers: Automatic Change Tracking

Database triggers can automatically capture changes to sensitive data for audit purposes. An audit trigger logs who changed what, when, and the old and new values. This provides a reliable audit trail that cannot be bypassed.

## Audit Table Design

The audit table captures the table name, operation type (INSERT, UPDATE, DELETE), the old row values, the new row values, the user who made the change, and a timestamp. For compliance, include the application context—the session ID, IP address, and transaction ID.

## Trigger Implementation

Each audited table gets a trigger that fires on INSERT, UPDATE, DELETE. The trigger function captures the OLD and NEW row values and inserts into the audit table. Row-level triggers capture individual row changes with full context.

## Performance Considerations

Audit triggers add overhead to every DML operation. Batch the audit writes when possible. Consider asynchronous audit logging for high-traffic tables. Archive audit data regularly. Index the audit table on timestamp and table name for efficient queries.

## Compliance

Audit logs support SOX, HIPAA, PCI-DSS, and SOC 2 compliance. They provide evidence of data access and modification. Keep audit logs immutable—restrict write access and set retention policies. Test audit coverage regularly.

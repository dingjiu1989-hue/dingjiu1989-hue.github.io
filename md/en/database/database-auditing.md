---
title: "Database Auditing: Tracking Data Changes"
description: "Implement database auditing to track who changed what and when for compliance, security, and debugging."
date: 2026-04-13
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-auditing.html
---

# Database Auditing: Tracking Data Changes

Database auditing tracks data changes for compliance, security, and debugging. A comprehensive audit system records who changed what, when the change occurred, the old and new values, and the context of the change.

## Audit Strategies

Trigger-based auditing uses database triggers to capture changes. An audit trigger fires on INSERT, UPDATE, or DELETE operations and writes change records to an audit table. This approach captures all changes regardless of how they reach the database—application code, admin tools, or direct SQL.

Application-level auditing logs changes in the application layer. Each service explicitly writes audit records when it modifies data. This provides richer context (user ID, request ID, business reason) but only captures changes made through the application.

Change Data Capture (CDC) streams database changes to a log (like Kafka) for external consumers. Debezium is the most popular CDC tool. It reads the database transaction log and publishes change events without modifying application code.

## Audit Table Design

A minimal audit table includes: audit_id (primary key), table_name, row_id, operation (INSERT, UPDATE, DELETE), old_values (JSON), new_values (JSON), changed_by, changed_at, transaction_id. Consider partitioning by date for query performance.

Include a session context so you know not just who changed data but under what circumstances. Store API endpoint, IP address, and correlation ID if available.

## Querying Audit Data

Audit tables grow quickly. Index by table_name + row_id for point queries, by changed_at for time-based queries, and by changed_by for user activity audits. Consider archiving old audit records to cost-effective storage. Set retention policies based on compliance requirements.

## Performance Impact

Writing audit records adds latency to every data modification. Consider asynchronous auditing—write to a queue and process audit records in the background. Batch audit writes to reduce database transaction overhead. Monitor audit queue depth to detect processing bottlenecks.

## Compliance

Many regulations require audit trails. GDPR requires tracking personal data access. SOX requires financial data change tracking. PCI-DSS requires audit trails for cardholder data. Design your audit system to meet the strictest relevant regulation.

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>).

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>)

**See also:** [Change Data Capture: Tracking Database Changes in Real-Time](</en/database/database-change-tracking-cdc.html>), [Database Audit Triggers: Automatic Change Tracking](</en/database/database-audit-triggers.html>), [Database Encryption: Data at Rest and in Transit](</en/database/database-encryption.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Design Patterns: Repository, Unit of Work, Query Objects, Table Inheritance](</en/database/database-design-patterns.html>), [Geospatial Data with PostGIS: Geometry, Geography, and Spatial Queries](</en/database/geospatial-data.html>)

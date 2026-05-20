---
title: "Database Cost Optimization: Instance Sizing, Reserved Instances, Storage Tiering"
description: "Learn database cost optimization strategies: right-sizing instances, reserved instances, storage tiering, serverless databases, and practical cost-saving techniques."
date: 2026-04-02
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-cost-optimization.html
---

# Database Cost Optimization: Instance Sizing, Reserved Instances, Storage Tiering

Database Cost Optimization: Instance Sizing, Reserved Instances, Storage Tiering 

Database costs are often the largest infrastructure expense for data-intensive applications. This article covers strategies to optimize database spending without sacrificing performance or reliability. 

Right-Sizing Instances 

Over-provisioning is the most common cause of wasted database spend. Most teams provision for peak load and never scale down. 

Measuring Utilization 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- CPU utilization (via pg_stat_statements)

SELECT ROUND(AVG(extract(epoch FROM total_exec_time) / calls), 2) AS avg_query_time

FROM pg_stat_statements;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Connection utilization

SELECT count(*) AS connections, setting AS max_connections

FROM pg_settings, pg_stat_activity

WHERE name = 'max_connections'

GROUP BY setting;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Disk IOPS

SELECT schemaname, tablename,

seq_tup_read, idx_tup_fetch,

seq_scan, idx_scan

FROM pg_stat_user_tables

ORDER BY seq_scan DESC;

In cloud environments, monitor CloudWatch (AWS), Azure Monitor, or GCP Cloud Monitoring metrics: 

  * **CPU Utilization** : If consistently below 20%, downsize.

  * **Database Connections** : If below 30% of max, reduce max_connections or instance size.

  * **Read/Write IOPS** : Provisioned IOPS that are never used are pure waste.

  * **Storage Used** : Wasted storage costs money; reclaim unused space.




The Sizing Process 

## Before: 8 vCPU, 32 GB RAM, 1000 GB gp2 ($700/month)

## After monitoring for 2 weeks:

## Peak CPU: 25%, average CPU: 12%

## Peak connections: 40 of 200

## Storage used: 120 GB

## Optimized: 4 vCPU, 16 GB RAM, 150 GB gp3 ($200/month - 71% savings)

Reserved Instances 

Cloud providers offer significant discounts for committing to 1-year or 3-year terms: 

| Commitment | AWS RDS Discount | Azure SQL Discount | GCP Cloud SQL | |------------|-----------------|-------------------|---------------| | 1-year no upfront | ~30% | ~30% | ~25% | | 1-year partial upfront | ~35% | ~35% | ~30% | | 3-year all upfront | ~60% | ~55% | ~50% | 

When to Reserve 

  * **Reserve when** : Workload is predictable and runs 24/7. Production databases are ideal.

  * **Do not reserve when** : Development/staging instances that run only during business hours. Short-lived project databases.




Using Reserved Instances with Auto-Scaling 

If you use read replicas that scale dynamically, consider a mixed strategy: 

Production primary: 3-year reserved instance (60% savings)

Read replicas (fixed): 1-year reserved (30% savings)

Read replicas (auto-scaling): On-demand (flexibility premium)

Storage Tiering 

Different data needs different storage performance: 

AWS RDS Storage Options 

| Type | IOPS/GB | Max IOPS | Cost/GB/Month | Use Case | |------|---------|----------|---------------|----------| | gp2 | 3 baseline | 16,000 | $0.10 | Development, low-throughput workloads | | gp3 | 3,000 baseline | 16,000 | $0.08 | General purpose (cheaper than gp2) | | io1 | Provisioned | 256,000 | $0.125 + IOPS | High-throughput OLTP | | io2 | Provisioned | 256,000 | $0.125 + IOPS | Mission-critical, 99.999% durability | 

Storage Tiering Strategy 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Move historical data to cheaper storage

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- 1. Partition by date

CREATE TABLE orders (

id BIGSERIAL,

created_at TIMESTAMPTZ NOT NULL,

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- ...

) PARTITION BY RANGE (created_at);

CREATE TABLE orders_current PARTITION OF orders

FOR VALUES FROM ('2026-01-01') TO ('2027-01-01')

TABLESPACE fast_ssd;

CREATE TABLE orders_archive PARTITION OF orders

FOR VALUES FROM ('2020-01-01') TO ('2025-01-01')

TABLESPACE cold_hdd;

S3 Integration for Long-Term Storage 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Using pg_export or custom archival to S3

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Archive older partitions to S3

SELECT aws_s3.query_export_to_s3(

'SELECT * FROM orders WHERE created_at < ''2025-01-01''',

's3://myapp-backups/archived_orders/',

'orders_20250101.csv'

);

DROP TABLE orders_archive;

Serverless Databases 

Serverless databases (Aurora Serverless, Cloud SQL, Azure Serverless) scale compute automatically and charge only for usage: 

Aurora Serverless v2 

## Automatic scaling from 0.5 to 64 ACUs

## 1 ACU = ~2 GB RAM, proportional CPU

aurora:

engine: aurora-postgresql

serverlessv2:

min_capacity: 0.5

max_capacity: 16

scaling_configuration:

seconds_until_auto_pause: 300

auto_pause: true

Cost scenarios: 

| Workload | Traditional (db.r6g.large) | Serverless | |----------|---------------------------|------------| | 24/7 moderate | $170/month | $180/month (slightly more) | | Development (8 hours/day) | $170/month | $60/month (65% savings) | | Spiky/unpredictable | $340/month (over-provisioned) | $120/month (65% savings) | 

Data Compression Savings 

As discussed in the compression article, compression directly reduces storage costs: 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Before: 200 GB table on gp3 ($16/month)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- After page compression with zstd: 60 GB ($5/month)

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Savings: $11/month per table

ALTER TABLE large_logs SET (compression = 'zstd');

Practical Cost-Saving Checklist 

  * [ ] Right-size instances based on 2-week utilization data.

  * [ ] Purchase reserved instances for production databases.

  * [ ] Use gp3 instead of gp2 (same performance, lower cost).

  * [ ] Archive or delete unused data.

  * [ ] Remove unused indexes (each index adds write overhead and storage cost).

  * [ ] Enable compression on compressible data.

  * [ ] Use read replicas instead of larger instances for read scaling.

  * [ ] Consider serverless for development and variable workloads.

  * [ ] Set storage autoscaling with limits to prevent runaway costs.

  * [ ] Monitor and alert on cost anomalies.




Monitoring Cost Efficiency 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- Track wasted storage: dead tuples

SELECT schemaname, tablename,

n_dead_tup * 8192 AS wasted_bytes

FROM pg_stat_user_tables

ORDER BY wasted_bytes DESC;

Set up cloud cost budgets and alerts: 

## AWS Budget example

aws budgets create-budget \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--account-id 123456789012 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--budget file://budget.json

## Alert at 80% and 100% of monthly budget

Database cost optimization is an ongoing practice, not a one-time project. Review your database costs quarterly, right-size based on actual usage patterns, and leverage cloud provider discounts for predictable workloads.

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>).

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database Compression: Page-Level, Tuple-Level, Columnar, and TOAST](</en/database/database-compression.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

**See also:** [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>), [EXPLAIN ANALYZE Deep Dive: Reading Plans, Cost Estimation, and Scan Types](</en/database/query-optimization-explain.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>)

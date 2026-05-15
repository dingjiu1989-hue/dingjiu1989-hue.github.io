---
title: "Database Disaster Recovery: RPO, RTO, Cross-Region Replication"
description: "Learn database disaster recovery planning: RPO and RPO definitions, cross-region replication strategies, backup testing, and DR drill execution."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-disaster-recovery.html
---

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

# Database Disaster Recovery: RPO, RTO, Cross-Region Replication

Database Disaster Recovery: RPO, RTO, Cross-Region Replication 

Disaster recovery (DR) ensures your database can survive catastrophic events: region outages, data corruption, accidental deletions, or ransomware attacks. Unlike high availability, which handles component failures, DR addresses large-scale disasters. 

RPO and RTO 

Two metrics define DR requirements: 

**Recovery Point Objective (RPO)** : The maximum acceptable data loss measured in time. An RPO of 1 hour means you can lose at most 1 hour of data. 

**Recovery Time Objective (RTO)** : The maximum acceptable downtime. An RTO of 4 hours means the database must be operational within 4 hours of the disaster. 

| Scenario | RPO | RTO | Strategy | |----------|-----|-----|----------| | Internal tool | 24 hours | 24 hours | Daily backups, restore | | E-commerce | 5 minutes | 1 hour | Cross-region replication | | Financial trading | 0 (zero loss) | 5 minutes | Synchronous replication + DR site | 

Cross-Region Replication 

PostgreSQL Logical Replication Across Regions 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- On primary (us-east-1)

CREATE PUBLICATION dr_pub FOR ALL TABLES;

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- On standby (us-west-2)

CREATE SUBSCRIPTION dr_sub

CONNECTION 'host=primary-us-east-1.example.com port=5432 dbname=proddb'

PUBLICATION dr_pub

WITH (copy_data = true, connect = true, create_slot = true);

Logical replication works across regions with asynchronous delivery. Monitor lag carefully: 

SELECT pg_size_pretty(

pg_wal_lsn_diff(

pg_current_wal_lsn(),

replay_lsn

)

) AS replication_lag

FROM pg_stat_replication

WHERE application_name = 'dr_sub';

AWS RDS Cross-Region Read Replicas 

# Create cross-region read replica

aws rds create-db-instance-read-replica \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--db-instance-identifier mydb-dr \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--source-db-instance-identifier mydb \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--region us-west-2 \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--db-instance-class db.r6g.large

# Promote to standalone for DR

aws rds promote-read-replica \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--db-instance-identifier mydb-dr \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--region us-west-2

Multi-Region with Patroni 

Patroni can manage clusters across regions with careful configuration: 

# DR site configuration

scope: myapp

namespace: /service/

name: pg-dr-node-1

consul:

host: dr-consul.service.consul:8500

# Separate DCS for DR isolation

tags:

nofailover: true # DR site should not automatically become primary

Backup-Based DR 

For cost-sensitive environments, backups plus WAL archiving to S3 provide DR: 

# Continuous WAL archiving to cross-region S3 bucket

archive_command = 'aws s3 cp %p s3://myapp-wal-dr/region/us-east-1/%f'

# DR restore procedure

pg_restore --dbname=proddb /backups/dr/latest_full.dump

pg_receivewal --directory /backups/dr/wal

Recovery Workflow 

# !/bin/bash

# Dr: restore to us-west-2

# 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Restore latest full backup

pgbackrest --stanza=prod --db-path=/var/lib/postgresql/dr restore

# 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Set recovery target

cat >> /var/lib/postgresql/dr/postgresql.conf << EOF

restore_command = 'aws s3 cp s3://myapp-wal-dr/region/us-east-1/%f %p'

recovery_target_time = '2026-05-12 10:00:00 UTC'

recovery_target_action = promote

EOF

# 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Start and recover

pg_ctl start -D /var/lib/postgresql/dr

# 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Verify data integrity

psql -c "SELECT count(*) FROM critical_table;"

psql -c "SELECT max(created_at) FROM orders;"

Backup Testing 

Backups are worthless until proven restorable. Regular testing is mandatory. 

Automated Restore Test 

# !/bin/bash

# Weekly restore test

set -euo pipefail

TEST_DIR=/tmp/dr_test_$(date +%Y%m%d)

LOG_FILE=$TEST_DIR/restore.log

mkdir -p $TEST_DIR

echo "=== DR Restore Test $(date) ===" >> $LOG_FILE

# Full restore

pgbackrest --stanza=prod --db-path=$TEST_DIR/data restore >> $LOG_FILE 2>&1

# Start database

pg_ctl -D $TEST_DIR/data -l $TEST_DIR/pg.log start >> $LOG_FILE 2>&1

sleep 5

# Verify

echo "Database size:"

psql -p 5433 -c "SELECT pg_size_pretty(pg_database_size('proddb'));"

echo "Row counts:"

psql -p 5433 -c "

SELECT 'users' as tbl, count(*) FROM users

UNION ALL

SELECT 'orders', count(*) FROM orders

UNION ALL

SELECT 'payments', count(*) FROM payments;

"

echo "Max dates (data freshness):"

psql -p 5433 -c "

SELECT 'users' as tbl, max(created_at) FROM users

UNION ALL

SELECT 'orders', max(created_at) FROM orders;

"

# Cleanup

pg_ctl -D $TEST_DIR/data stop >> $LOG_FILE 2>&1

rm -rf $TEST_DIR

echo "=== Test Complete ===" >> $LOG_FILE

Schedule this via cron: 

0 2 * * 0 /usr/local/bin/dr_restore_test.sh

DR Plan Components 

A complete DR plan should document: 

  * **Contact list** : Who to contact and escalation paths.



2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **RTO and RPO targets** : Specific to each data tier. 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Runbook** : Step-by-step recovery procedures. 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **DR site details** : Region, connection strings, credentials. 5\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Validation steps** : How to verify the recovery succeeded. 6\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Communication plan** : Internal and external notifications. 7\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. **Post-mortem process** : How to document and improve. 

Disaster Scenarios and Mitigations 

| Scenario | Mitigation | RPO Impact | |----------|------------|------------| | Region outage | Cross-region replica promotion | RPO = replication lag | | Accidental DROP TABLE | PITR to before the statement | RPO = time since last WAL backup | | Ransomware | Immutable WAL backups | RPO depends on backup frequency | | Data corruption | Replay WAL; keep multiple backups | Dependent on detection time | 

Testing DR with Chaos Engineering 

# Simulate region failure: block traffic to primary

iptables -A INPUT -s dr-test-region -j DROP

# Trigger DR failover script

./dr_failover.sh --target us-west-2

# Verify applications work from DR region

curl -f https://dr-api.myapp.com/health

# Fail back

./dr_failback.sh --target us-east-1

# Clean up

iptables -D INPUT -s dr-test-region -j DROP

Run DR drills quarterly at minimum. Document every drill outcome and update the runbook with lessons learned. A DR plan that has never been tested is not a plan; it is a hope.

**See also:** [Database Migration Strategies](</en/database/database-migration-strategies.html>), [Database Horizontal Scaling Strategies](</en/database/database-horizontal-scaling.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>).

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Capacity Planning: Sizing, Growth Forecasting, and Scaling](</en/database/database-capacity-planning.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

---
title: "Database Backup and Recovery Strategies"
description: "Learn database backup strategies including full, incremental, and differential backups, point-in-time recovery, and disaster recovery planning."
date: 2026-05-11
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-backup-strategies.html
---

## Why Backup Strategies Matter

Data loss happens. Hardware fails, software bugs corrupt data, human errors delete tables, and ransomware encrypts databases. A robust backup strategy is your last line of defense. Recovery ability, not backup creation, is what matters.

## The RPO and RPO Framework

| Metric | Definition | Example |
|--------|------------|---------|
| RPO (Recovery Point Objective) | Maximum acceptable data loss | 1 hour = lose at most 1 hour of data |
| RTO (Recovery Time Objective) | Maximum acceptable downtime | 4 hours = must recover within 4 hours |
| WRT (Workload Recovery Time) | Time to make application functional | RTO includes WRT |

### Setting Targets

| Application Type | RPO | RTO |
|-----------------|-----|-----|
| Banking transaction system | < 1 minute | < 5 minutes |
| E-commerce platform | < 5 minutes | < 1 hour |
| Content management system | < 1 hour | < 4 hours |
| Analytics/reporting | < 24 hours | < 24 hours |
| Development/staging | Best effort | < 48 hours |

## Backup Types

### Full Backup

A complete copy of the entire database. Slowest to create, fastest to restore.

```bash
# PostgreSQL full backup
pg_dump -h localhost -U app_user -F c -f /backups/daily/full_$(date +%Y%m%d).dump mydb

# MySQL full backup
mysqldump -h localhost -u app_user -p mydb > /backups/daily/full_$(date +%Y%m%d).sql

# MongoDB full backup
mongodump --host localhost --db mydb --out /backups/daily/$(date +%Y%m%d)
```

### Incremental Backup

Backs up only data changed since the last backup of any type. Fastest to create, slowest to restore.

### Differential Backup

Backs up data changed since the last full backup. Faster to restore than incremental.

| Metric | Full | Incremental | Differential |
|--------|------|-------------|--------------|
| Backup size | Largest | Smallest | Medium |
| Backup time | Slowest | Fastest | Medium |
| Restore time | Fastest | Slowest | Medium |
| Frequency | Weekly | Daily/hourly | Daily |

## Point-in-Time Recovery (PITR)

PITR allows restoring a database to any point in time by replaying WAL (Write-Ahead Log) segments.

### PostgreSQL WAL Archiving

```bash
# postgresql.conf
wal_level = replica
archive_mode = on
archive_command = 'test ! -f /backups/wal/%f && cp %p /backups/wal/%f'
archive_timeout = 60  # Force WAL switch every 60 seconds

# Full base backup
pg_basebackup -h localhost -D /backups/base/$(date +%Y%m%d) -X stream -P
```

### Restoring to a Point in Time

```bash
# 1. Restore base backup
cp -R /backups/base/20260511 /var/lib/postgresql/16/main

# 2. Configure recovery (recovery.conf)
restore_command = 'cp /backups/wal/%f %p'
recovery_target_time = '2026-05-11 14:23:45'
recovery_target_action = promote

# 3. Start PostgreSQL; it replays WAL to the target time
pg_ctl start
```

### Automated PITR with pgBackRest

```bash
# pgbackrest.conf
[global]
repo1-path=/backups/pgbackrest
repo1-retention-full=4
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=secure_backup_password

[main]
pg1-path=/var/lib/postgresql/16/main

# Create full backup
pgbackrest --stanza=main --type=full backup

# Create incremental backup
pgbackrest --stanza=main --type=incr backup

# List backups
pgbackrest --stanza=main info

# Restore to specific timestamp
pgbackrest --stanza=main --type=time --target="2026-05-11 14:23:45" restore
```

## Cloud Backup Strategies

### AWS RDS Automated Backups

```bash
# Automated backups are enabled by default (7 day retention)
aws rds modify-db-instance \
    --db-instance-identifier mydb \
    --backup-retention-period 35  # Extend to 35 days max

# Manual snapshot
aws rds create-db-snapshot \
    --db-instance-identifier mydb \
    --db-snapshot-identifier mydb-pre-migration-snapshot

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier mydb-restored \
    --db-snapshot-identifier mydb-pre-migration-snapshot

# Point-in-time restore
aws rds restore-db-instance-to-point-in-time \
    --source-db-instance-identifier mydb \
    --target-db-instance-identifier mydb-restored \
    --restore-time "2026-05-11T14:23:45Z"
```

### GCP Cloud SQL

```bash
# Enable PITR (binary logging)
gcloud sql instances patch mydb \
    --enable-bin-log \
    --backup-start-time=23:00

# Create backup
gcloud sql backups create --instance=mydb

# List backups
gcloud sql backups list --instance=mydb

# Restore
gcloud sql backups restore --restore-instance=mydb-restored \
    --backup-id=123456
```

## Backup Verification

A backup that cannot be restored is worthless. Test your backups regularly:

```bash
#!/bin/bash
# Weekly restore test script

# Restore backup to test environment
pg_restore -d test_db /backups/daily/full_latest.dump

# Run integrity checks
psql -d test_db -c "SELECT count(*) FROM information_schema.tables;"
psql -d test_db -c "SELECT count(*) FROM users;"

# Compare record counts with production
prod_count=$(psql -d production_db -c "SELECT count(*) FROM users" -t)
test_count=$(psql -d test_db -c "SELECT count(*) FROM users" -t)

if [ "$prod_count" -eq "$test_count" ]; then
    echo "Backup verification PASSED"
else
    echo "Backup verification FAILED: count mismatch"
fi

# Clean up
dropdb test_db
```

## Backup Automation

```yaml
# Backup cron schedule
# Daily full backup at 2 AM
0 2 * * * /usr/local/bin/backup_full.sh
# WAL archiving every 5 minutes (handled by PostgreSQL)

# Weekly verification
0 6 * * 1 /usr/local/bin/test_restore.sh

# Monthly copy to cold storage
0 4 1 * * /usr/local/bin/archive_to_s3.sh
```

## 3-2-1 Backup Rule

| Rule | Explanation | Implementation |
|------|-------------|----------------|
| 3 copies of data | Production + 2 backups | Live DB + local backup + remote backup |
| 2 different media types | Different failure modes | SSD + tape/cloud storage |
| 1 off-site copy | Disaster recovery | S3, GCS, or another region |

## Disaster Recovery Scenarios

| Scenario | Recovery Method | RTO |
|----------|----------------|-----|
| Accidental DELETE | PITR to just before the statement | 30 min |
| Table corruption | Restore full + PITR to last consistent state | 2 hours |
| Entire instance failure | Restore from latest full backup on new instance | 4 hours |
| Region outage | Cross-region replica promotion or backup restore | 1-8 hours |
| Ransomware | Restore from backup before encryption timestamp | 2 hours |

## Summary

Define your RPO and RPO targets before designing backup strategies. Use full backups for weekly snapshots, continuous WAL archiving for point-in-time recovery, and verify backups regularly by testing restores. Follow the 3-2-1 rule for data protection, automate the entire process, and document recovery procedures so anyone on the team can execute a restore. A backup that has never been tested is not a backup; it is a hope.

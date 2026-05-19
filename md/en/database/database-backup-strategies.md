---
title: "Database Backup and Recovery Strategies"
description: "Learn database backup strategies including full, incremental, and differential backups, point-in-time recovery, and disaster recovery planning."
date: 2025-12-22
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-backup-strategies.html
---

# Database Backup and Recovery Strategies

RPO and RTO 

RPO (Recovery Point Objective): Maximum acceptable data loss. RTO (Recovery Time Objective): Maximum acceptable downtime. 

| System | RPO | RTO | |--------|-----|-----| | Banking | < 1 min | < 5 min | | E-commerce | < 5 min | < 1 hour | | Analytics | < 24 hours | < 24 hours | 

Backup Types 

| Type | Size | Speed | Restore | |------|------|-------|---------| | Full | Largest | Slowest | Fastest | | Incremental | Smallest | Fastest | Slowest | | Differential | Medium | Medium | Medium | 

Point-in-Time Recovery (WAL Archiving) 

## postgresql.conf

wal_level = replica

archive_mode = on

archive_command = 'cp %p /backups/wal/%f'

archive_timeout = 60

## Full base backup

pg_basebackup -h localhost -D /backups/base/$(date +%Y%m%d) -X stream -P

## Restore to point in time

## recovery.conf

restore_command = 'cp /backups/wal/%f %p'

recovery_target_time = '2026-05-11 14:23:45'

Cloud Backups 

## AWS RDS

aws rds create-db-snapshot --db-instance-identifier mydb

aws rds restore-db-instance-from-db-snapshot \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--db-instance-identifier mydb-restored \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--db-snapshot-identifier mydb-snapshot

## Point-in-time restore

aws rds restore-db-instance-to-point-in-time \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--source-db-instance-identifier mydb \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--target-db-instance-identifier mydb-restored \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--restore-time "2026-05-11T14:23:45Z"

The 3-2-1 Rule 

3 copies of data, 2 different media types, 1 off-site copy. Test restores regularly. 

Conclusion 

Define RPO/RTO before designing backup strategy. Use continuous WAL archiving for PITR. Follow the 3-2-1 rule. Test restores regularly. Automate the entire process.

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>).

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Database Backup Types: Full, Incremental, Differential, WAL Archiving](</en/database/backup-types.html>), [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Migration Tools and Strategies](</en/database/database-migration.html>)

**See also:** [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

**See also:** [Database Testing Strategies for Developers](</en/database/database-testing.html>), [Data Modeling Best Practices](</en/database/data-modeling.html>), [Database Indexing Strategies](</en/database/database-indexing.html>)

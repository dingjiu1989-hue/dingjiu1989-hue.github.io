---
title: "Database Backup Types: Full, Incremental, Differential, WAL Archiving"
description: "Explore database backup strategies including full, incremental, differential backups, WAL archiving, and point-in-time recovery with PostgreSQL."
date: 2026-03-30
board: database
url: https://dingjiu1989-hue.github.io/en/database/backup-types.html
---

# Database Backup Types: Full, Incremental, Differential, WAL Archiving

Database Backup Types: Full, Incremental, Differential, WAL Archiving 

No database backup strategy is complete until it has been tested with a real restoration. This article covers backup types, PostgreSQL-specific tools, and how to implement point-in-time recovery (PITR). 

Backup Types 

Full Backup 

A full backup copies the entire database cluster. It is the foundation of any backup strategy. 

## PostgreSQL full backup with pg_dump (logical)

pg_dump -h localhost -U admin -Fc -f prod_backup.dump proddb

## Or directory format for parallel dumps

pg_dump -h localhost -U admin -Fd -j 4 -f /backups/proddb proddb

## Physical full backup with pg_basebackup

pg_basebackup -h localhost -U replicator \

-D /backups/full/$(date +%Y%m%d) \

-X stream -P -v

**Pros** : Complete snapshot, simple restoration. **Cons** : Large, time-consuming, resource-intensive. 

Incremental Backup 

An incremental backup captures only changes since the last backup (of any type). PostgreSQL achieves this via WAL archiving: 

## Archive WAL segments continuously

## In postgresql.conf:

archive_mode = on

archive_command = 'cp %p /backups/wal/%f'

Each 16 MB WAL segment is an incremental backup. 

Differential Backup 

A differential backup captures changes since the last full backup. It is larger than an incremental but faster to restore (only the full + one differential needed). 

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\-- pgBackRest differential backup

pgbackrest --stanza=prod --type=diff backup

WAL Archiving and Point-in-Time Recovery 

WAL archiving is PostgreSQL's mechanism for continuous archiving. Combined with a base backup, it enables restoring to any point in time. 

Configuration 

## postgresql.conf

wal_level = replica

archive_mode = on

archive_command = 'aws s3 cp %p s3://my-backups/wal/%f'

archive_timeout = 60

Recovery 

To restore to a specific point in time: 

## recovery.signal (or standby.signal for replica)

restore_command = 'aws s3 cp s3://my-backups/wal/%f %p'

recovery_target_time = '2026-05-10 14:30:00 UTC'

recovery_target_action = promote

Start PostgreSQL. It replays WAL segments until it reaches the target time and then promotes itself to a primary. 

Complete PITR Workflow 

## 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Take a base backup

pg_basebackup -h prod-db -U replicator -D /backups/base_20260512 -X stream

## 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Archive WAL continuously (configured in postgresql.conf)

## 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\. Restore to a point in time

mkdir /var/lib/postgresql/restored

cp -r /backups/base_20260512/* /var/lib/postgresql/restored/

touch /var/lib/postgresql/restored/recovery.signal

cat > /var/lib/postgresql/restored/postgresql.conf << EOF

restore_command = 'aws s3 cp s3://my-backups/wal/%f %p'

recovery_target_time = '2026-05-12 03:15:00 UTC'

recovery_target_action = promote

EOF

pg_ctl start -D /var/lib/postgresql/restored

Backup Strategies Compared 

| Type | Size | Restore Speed | Complexity | Frequency | |------|------|---------------|------------|-----------| | Full | Largest | Slowest | Low | Weekly | | Incremental | Smallest | Slowest | Medium | Continuous | | Differential | Medium | Medium | Medium | Daily | | WAL archiving | Tiny per segment | Fast (with base) | High | Continuous | 

pg_dump vs pg_basebackup 

Use `pg_dump` for: 

  * Logical backup of specific databases or schemas.

  * Porting to a different PostgreSQL version or architecture.

  * Selective restoration (single table or schema).




Use `pg_basebackup` for: 

  * Full-cluster physical backup.

  * Setting up streaming replicas.

  * Point-in-time recovery capability.

  * Faster bulk restore (skip SQL parsing).




pgBackRest 

pgBackRest is the most popular dedicated backup tool for PostgreSQL: 

## Configure stanza

pgbackrest --stanza=prod stanza-create

## Full backup

pgbackrest --stanza=prod --type=full backup

## Incremental backup (default)

pgbackrest --stanza=prod --type=incr backup

## List backups

pgbackrest --stanza=prod info

## Restore to specific point

pgbackrest --stanza=prod --type=time \

\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\--target="2026-05-12 03:15:00" restore

Testing Backups 

A backup that cannot be restored is worthless. Regular restore testing is mandatory: 

## Automated restore test script

## !/bin/bash

set -e

RESTORE_DIR=/tmp/restore_test

BACKUP_DIR=/backups/weekly

rm -rf $RESTORE_DIR

pgbackrest --stanza=prod --db-path=$RESTORE_DIR restore

pg_ctl start -D $RESTORE_DIR -l $RESTORE_DIR/logfile

sleep 10

psql -d postgres -c "SELECT count(*) FROM pg_database;"

pg_ctl stop -D $RESTORE_DIR

rm -rf $RESTORE_DIR

echo "Restore test PASSED at $(date)"

Cloud Backup Integration 

Most cloud providers offer managed backup services: 

  * **RDS Automated Backups** : Daily snapshot + 5 minutes of WAL. PITR enabled by default.

  * **Cloud SQL** : Point-in-time recovery with binary log archiving.

  * **Aurora** : Continuous backup to S3 with PITR, no performance impact.




The 3-2-1 rule applies to databases: three copies of data, on two different media, with one off-site. Your backup strategy should verify all three conditions regularly.

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database Table Partitioning: Range, List, Hash](</en/database/database-partitioning.html>).

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Database Backup Strategies to Object Storage](</en/database/database-backup-to-s3.html>), [Database Backup and Recovery Strategies](</en/database/database-backup-strategies.html>), [Database High Availability: Failover, Standby Types, Health Checks](</en/database/database-high-availability.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

**See also:** [Multi-Master Replication: Conflict Resolution, CRDTs, Galera, and BDR](</en/database/multi-master-replication.html>), [Read Replicas: Scaling Reads, Replication Lag, and Failover](</en/database/read-replicas.html>), [NoSQL Databases Guide](</en/database/nosql-guide.html>)

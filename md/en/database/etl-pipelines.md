---
title: "Building ETL Pipelines: A Practical Guide"
description: "Practical ETL guide covering batch vs streaming, Airflow, dbt, Fivetran, data quality checks, incremental loads, and idempotency."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/etl-pipelines.html
---

ETL (Extract, Transform, Load) pipelines are the backbone of data engineering. They move data from source systems to data warehouses, transform it into analytical models, and ensure it is reliable and current. This article covers the practical aspects of building ETL pipelines that are reliable, maintainable, and scalable.

## Batch vs Streaming

### Batch Processing

Batch pipelines process data in chunks at scheduled intervals. They are simpler to build, easier to test, and cheaper to run.

**When to use batch**:
- Data freshness requirements are hourly or daily.
- Source systems do not support real-time streaming.
- Complex transformations require full dataset scans.
- Cost optimization is a priority.

```python
# Simple batch ETL with Apache Airflow
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd

def extract_orders():
    return pd.read_sql("SELECT * FROM orders WHERE date = CURRENT_DATE",
                       conn_string)

def transform_orders(orders_df):
    # Clean and transform
    orders_df['total'] = orders_df['quantity'] * orders_df['price']
    orders_df['order_month'] = orders_df['order_date'].dt.to_period('M')
    return orders_df

def load_orders(transformed_df):
    transformed_df.to_sql('daily_orders', data_warehouse_conn,
                          if_exists='append', index=False)

default_args = {
    'owner': 'data_team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG('orders_etl',
         default_args=default_args,
         schedule_interval='0 6 * * *',
         start_date=datetime(2026, 1, 1)):
    extract = PythonOperator(task_id='extract', python_callable=extract_orders)
    transform = PythonOperator(task_id='transform', python_callable=transform_orders)
    load = PythonOperator(task_id='load', python_callable=load_orders)

    extract >> transform >> load
```

### Stream Processing

Streaming pipelines process data as it arrives, with millisecond to second latency.

**When to use streaming**:
- Real-time dashboards and alerts.
- Event-driven architectures.
- High-velocity data (IoT, clickstream, logs).
- Fraud detection and monitoring.

```python
# Streaming ETL with Kafka + Faust
import faust

class Order(faust.Record):
    order_id: str
    user_id: str
    product: str
    amount: float
    timestamp: str

app = faust.App('streaming_etl', broker='kafka://localhost:9092')
topic = app.topic('raw_orders', value_type=Order)
sink = app.topic('enriched_orders')

@app.agent(topic)
async def process_orders(orders):
    async for order in orders:
        # Enrich with user segment
        user_segment = await lookup_user_segment(order.user_id)
        enriched = {
            **order.__dict__,
            'user_segment': user_segment,
            'processing_time': datetime.utcnow().isoformat()
        }
        await sink.send(value=enriched)
```

### Lambda Architecture

Many organizations use a lambda architecture: batch for comprehensive, accurate views and streaming for real-time views. The two paths converge in the serving layer.

## Orchestration with Apache Airflow

Airflow is the most popular open-source workflow orchestrator. It schedules tasks, manages dependencies, and provides monitoring and alerting.

### DAG Design Principles

```python
# Airflow DAG with best practices
ETL_DAILY = {
    # 1. Use catchup=False to avoid backfilling old runs
    'catchup': False,
    # 2. Set meaningful retries with exponential backoff
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    # 3. Set SLA for data freshness
    'sla': timedelta(hours=8),
    # 4. Configure alerts
    'email_on_failure': True,
    'email': ['data-alerts@example.com'],
}
```

### Task Design Principles

1. **Idempotency**: Running a task multiple times should produce the same result.
2. **Atomicity**: Each task should do one thing and do it completely.
3. **Retryability**: Tasks should handle transient failures gracefully.
4. **Observability**: Log meaningful metrics for monitoring.

## Data Transformation with dbt

dbt (data build tool) has become the standard for SQL-based transformations in the warehouse. It handles the "T" in ELT — transformations happen inside the warehouse using SQL.

### dbt Models

```sql
-- models/staging/stg_orders.sql
-- Source: staging layer, minimal transformations
with source as (
    select * from {{ source('ecommerce', 'orders') }}
),

renamed as (
    select
        id as order_id,
        customer_id,
        order_date,
        status,
        amount
    from source
)

select * from renamed
```

```sql
-- models/marts/daily_customer_orders.sql
-- Mart: Business-facing aggregations
with orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customer_id,
        order_date,
        count(*) as order_count,
        sum(amount) as total_amount
    from orders
    group by 1, 2
)

select * from customer_orders
```

### dbt Testing

dbt provides built-in and custom tests for data quality.

```yaml
# schema.yml: Define tests on models
version: 2

models:
  - name: stg_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
      - name: status
        tests:
          - accepted_values:
              values: ['placed', 'shipped', 'completed', 'returned']

  - name: daily_customer_orders
    tests:
      - dbt_utils.expression_is_true:
          expression: "order_count >= 0"

  - name: order_total_consistency
    tests:
      - dbt_utils.expression_is_true:
          expression: "total_amount = (SELECT SUM(amount) FROM stg_orders)"
```

## Data Quality Checks

Data quality is not optional. Bad data leads to bad decisions.

### Categories of Data Quality

| Category | Description | Check |
|----------|-------------|-------|
| Completeness | Are all records present? | Row count comparison |
| Uniqueness | Are there duplicates? | Primary key uniqueness |
| Timeliness | Is data fresh enough? | Max timestamp check |
| Accuracy | Is the data correct? | Cross-source reconciliation |
| Consistency | Do related values agree? | Referential integrity |

```python
# Data quality check function
def run_data_quality_checks(warehouse_conn):
    checks = [
        {
            "name": "orders_completeness",
            "query": """
                SELECT 'orders' as table_name,
                       COUNT(*) as row_count,
                       CURRENT_TIMESTAMP as checked_at
                FROM orders
                WHERE order_date = CURRENT_DATE
            """,
            "threshold": lambda r: r['row_count'] > 1000,
            "severity": "critical"
        },
        {
            "name": "orders_freshness",
            "query": """
                SELECT MAX(order_date) as latest_order
                FROM orders
            """,
            "threshold": lambda r: r['latest_order'] >= CURRENT_DATE - INTERVAL '1 day',
            "severity": "warning"
        }
    ]

    for check in checks:
        result = execute_query(check["query"])
        if not check["threshold"](result):
            alert(f"DQ check failed: {check['name']}", check["severity"])
```

## Incremental Loads

Full refreshes do not scale for large datasets. Incremental loads process only new or changed data.

### Incremental Strategies

**Timestamp-based**: Track records by a `last_updated` or `created_at` column.

```sql
-- Incremental load: only new records
INSERT INTO warehouse.orders
SELECT * FROM source.orders
WHERE created_at > (SELECT MAX(created_at) FROM warehouse.orders);
```

**CDC (Change Data Capture)**: Capture insert, update, and delete events from the source database log. Tools like Debezium, Airbyte, and Fivetran implement CDC.

**Batch window**: Process data in time windows (daily partitions). Each run processes exactly one partition.

### Idempotency

Idempotent pipelines can be re-run safely. The output should be the same regardless of how many times the pipeline runs.

```sql
-- Idempotent insert: delete and re-insert
BEGIN;
DELETE FROM daily_orders WHERE order_date = '2026-05-12';
INSERT INTO daily_orders
SELECT * FROM source.orders WHERE order_date = '2026-05-12';
COMMIT;

-- Alternative: MERGE (upsert)
MERGE INTO daily_orders AS target
USING source.orders AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET
    status = source.status,
    amount = source.amount
WHEN NOT MATCHED THEN INSERT (order_id, ...)
    VALUES (source.order_id, ...);
```

## Managed ETL Services

For teams that want to avoid building and maintaining ETL infrastructure:

- **Fivetran**: Managed data pipeline service. Connects to 300+ sources and warehouses. Handles schema drift and incremental sync automatically.
- **Airbyte**: Open-source data integration platform. Self-hosted or cloud. Supports CDC and custom connectors.
- **Stitch**: Simple ETL service by Talend. Good for smaller teams.

## Conclusion

Build ETL pipelines that are idempotent, incremental, and observable. Use Airflow for orchestration, dbt for transformations, and implement data quality checks at every stage. Choose batch processing for simplicity and streaming for real-time needs. When in doubt, start with batch and add streaming where latency requirements demand it.

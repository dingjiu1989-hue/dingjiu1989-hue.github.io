---
title: "Data Warehousing Concepts and Modern Tools"
description: "Understand star schema vs snowflake, ETL/ELT, and modern data warehouses including Snowflake, BigQuery, Redshift, and materialized views."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/data-warehousing.html
---

# Data Warehousing Concepts and Modern Tools

Data Warehousing Concepts   
A data warehouse centralizes data from multiple sources for analysis and reporting. It is optimized for read-heavy analytical queries.   
Star Schema   
A central fact table connected to dimension tables:   

    
    
    CREATE TABLE fact_sales (
    
        sale_id BIGSERIAL PRIMARY KEY,
    
        date_key INT REFERENCES dim_date(date_key),
    
        product_key INT REFERENCES dim_product(product_key),
    
        customer_key INT REFERENCES dim_customer(customer_key),
    
        quantity INT NOT NULL,
    
        unit_price DECIMAL(10,2) NOT NULL,
    
        total_amount DECIMAL(12,2) GENERATED ALWAYS AS 
    
            (quantity * unit_price) STORED
    
    );
    
    
    
    CREATE TABLE dim_date (
    
        date_key INT PRIMARY KEY,
    
        date DATE NOT NULL, year SMALLINT, quarter SMALLINT,
    
        month SMALLINT, day SMALLINT, is_holiday BOOLEAN
    
    );
    
    

  
Snowflake Schema   
Normalized dimensions for storage efficiency. Dimensions are split into sub-dimensions, saving storage at the cost of more joins.   
ETL Pipeline   

    
    
    class ETLPipeline:
    
        def extract(self, query):
    
            return pd.read_sql(query, self.source_engine, chunksize=10000)
    
        
    
        def transform(self, df):
    
            df = df.drop_duplicates(subset=["order_id"])
    
            df["order_date"] = pd.to_datetime(df["order_date"])
    
            df["date_key"] = df["order_date"].dt.strftime("%Y%m%d").astype(int)
    
            return df
    
        
    
        def load(self, df, table_name):
    
            df.to_sql(table_name, self.warehouse_engine, if_exists="append", index=False)
    
    

  
Modern Data Warehousing   
Cloud data warehouses like Snowflake and BigQuery separate storage and compute, enabling elastic scaling. Materialized views pre-compute aggregations for dashboard queries.   
Conclusion   
Design with star schema for performance. Build resilient ETL pipelines. Leverage cloud warehouses for elastic scaling. Start simple and evolve.

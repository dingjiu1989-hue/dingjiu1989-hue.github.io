---
title: "Database Sharding: Strategies and Trade-offs"
description: "Explore key-based, range-based, and directory-based sharding strategies with rebalancing challenges and tools like Vitess and Citus."
date: 2026-05-12
board: database
url: https://dingjiu1989-hue.github.io/en/database/database-sharding.html
---

# Database Sharding: Strategies and Trade-offs

What is Sharding?   
Sharding splits a database across multiple servers horizontally. Each shard holds a subset of data, allowing linear scalability.   
Key-Based Sharding   
Hash the shard key to determine the target shard:   

    class KeyBasedShardManager:

        def __init__(self, num_shards=4):

            self.num_shards = num_shards

            self.shards = [Shard(i) for i in range(num_shards)]

        def get_shard(self, shard_key):

            hash_val = int(hashlib.sha256(str(shard_key).encode()).hexdigest(), 16)

            shard_id = hash_val % self.num_shards

            return self.shards[shard_id]

Range-Based Sharding   
Partition by value ranges:   

    CREATE TABLE orders (

        id BIGSERIAL, order_date DATE, total DECIMAL(10,2),

        PRIMARY KEY (id, order_date)

    ) PARTITION BY RANGE (order_date);

    CREATE TABLE orders_2026_01 PARTITION OF orders

        FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');

Directory-Based Sharding   
Use a lookup table for shard mapping:   

    class DirectoryShardManager:

        def __init__(self):

            self.directory = {}

        def map_key_to_shard(self, shard_key, shard_id):

            self.directory[shard_key] = shard_id

        def get_shard(self, shard_key):

            return self.directory.get(shard_key)

Rebalancing   
When adding or removing shards, data must be redistributed. Use consistent hashing to minimize data movement. Tools like Vitess and Citus automate this process.   
Conclusion   
Choose key-based sharding for even distribution, range-based for time-series data, and directory-based for maximum flexibility. Design shard keys carefully for even distribution. Plan for rebalancing from the start. Avoid cross-shard queries where possible.

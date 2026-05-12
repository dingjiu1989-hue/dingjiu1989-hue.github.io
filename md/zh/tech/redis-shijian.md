---
title: "Redis缓存实战：数据类型、过期策略、分布式锁实现"
description: "全面讲解Redis在实践中的核心用法，涵盖丰富的数据类型及应用场景、缓存过期与淘汰策略、分布式锁的实现方案和避坑指南。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/redis-shijian.html
---

## Redis数据类型与场景

Redis不仅是一个缓存，更是一个数据结构服务器。理解每种数据类型的特性和适用场景是充分发挥Redis能力的关键。

### String

最基本的数据类型，适合缓存、计数器、分布式ID等场景：

```bash
SET user:1001:name "张三"
INCR article:123:views
SETEX session:abc 3600 "user_data"  # 带过期时间的设置
```

### Hash

适合存储对象数据，可单独更新某个字段：

```bash
HSET user:1001 name "张三" age 28 city "北京"
HGET user:1001 name
HINCRBY user:1001 age 1
```

### List

基于链表实现，适合消息队列和时间线场景：

```bash
LPUSH timeline:user:1001 "post:1"
LRANGE timeline:user:1001 0 9  # 获取最近10条
```

### Set

无序集合，适合标签、去重和社交关系：

```bash
SADD article:1:tags "技术" "Redis" "缓存"
SINTER article:1:tags article:2:tags  # 共同标签
```

### Sorted Set

有序集合，适合排行榜、延迟队列等场景：

```bash
ZADD leaderboard 1000 "user1"
ZINCRBY leaderboard 10 "user1"
ZREVRANGE leaderboard 0 9 WITHSCORES  # Top 10
```

## 过期与淘汰策略

### 过期策略

Redis使用两种方式清理过期key：

- **惰性删除**：访问key时检查是否过期
- **定期删除**：每100ms随机检查一批key

### 内存淘汰策略

当内存达到上限时，根据配置的策略淘汰数据：

- **noeviction**：不淘汰，写入返回错误（默认）
- **allkeys-lru**：淘汰最近最少使用的key
- **volatile-lru**：仅在设置了过期时间的key中淘汰最少使用
- **allkeys-lfu**：淘汰最不频繁使用的key（Redis 4.0+）
- **volatile-ttl**：淘汰即将过期的key

建议生产环境使用`allkeys-lru`策略，配合合理的过期时间设置。

## 分布式锁

### 基本实现

使用SET命令的NX和EX参数实现：

```python
import redis

r = redis.Redis()

def acquire_lock(lock_name, acquire_timeout=10, lock_timeout=30):
    identifier = str(uuid.uuid4())
    end = time.time() + acquire_timeout
    while time.time() < end:
        if r.set(f"lock:{lock_name}", identifier, nx=True, ex=lock_timeout):
            return identifier
        time.sleep(0.01)
    return None

def release_lock(lock_name, identifier):
    # 使用Lua脚本保证原子性
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return r.eval(script, 1, f"lock:{lock_name}", identifier)
```

### Redlock算法

对于需要更高安全性的场景，可以使用Redlock算法在多个Redis节点上获取锁。

### 注意事项

- 锁的超时时间需要根据业务执行时间合理设置
- 使用唯一标识避免误删其他客户端持有的锁
- 释放锁时使用Lua脚本保证检查和删除的原子性
- 考虑可重入锁的需求

## 缓存常见问题

### 缓存穿透

查询不存在的数据导致请求直接打到数据库。

**解决方案**：缓存空值或使用布隆过滤器。

### 缓存击穿

热点key过期导致高并发请求直击数据库。

**解决方案：** 使用互斥锁或设置热点key永不过期。

### 缓存雪崩

大量key同时过期导致数据库压力激增。

**解决方案**：过期时间增加随机值，避免批量过期。

Redis作为高性能缓存和数据结构服务器，掌握其核心特性和常见问题的处理方案，是后端开发的必备技能。

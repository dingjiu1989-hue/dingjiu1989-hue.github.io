---
title: "Python异步编程：asyncio、协程、并发模式详解"
description: "系统讲解Python异步编程的核心概念和实践技巧，涵盖asyncio库使用、协程原理、并发模式设计和常见陷阱的深入分析。"
date: 2026-05-12
board: tech
url: https://dingjiu1989-hue.github.io/zh/tech/python-jin-cheng.html
---

## 异步编程基础

Python的异步编程通过asyncio库实现，核心概念包括协程、事件循环和Future。理解这些概念是掌握异步编程的前提。

## 协程与事件循环

### 协程的定义

协程是使用`async def`定义的函数，调用时返回一个协程对象：

```python
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

协程只有在事件循环中执行才会真正运行。

### 事件循环

事件循环是异步编程的核心调度器，负责管理所有待执行的协程：

```python
async def main():
    result = await fetch_data("https://api.example.com/data")

# Python 3.7+ 自动创建事件循环
asyncio.run(main())
```

## 并发执行模式

### 使用asyncio.gather

并发执行多个协程并等待所有完成：

```python
async def main():
    results = await asyncio.gather(
        fetch_data("https://api1.com"),
        fetch_data("https://api2.com"),
        fetch_data("https://api3.com"),
        return_exceptions=True  # 不因单个异常中断
    )
```

### 使用asyncio.create_task

创建后台任务，适用于不需要立即等待的场景：

```python
async def main():
    task1 = asyncio.create_task(fetch_data("url1"))
    task2 = asyncio.create_task(fetch_data("url2"))
    # 执行其他操作
    await asyncio.sleep(1)
    # 等待任务完成
    result1 = await task1
    result2 = await task2
```

## 高级模式

### 异步上下文管理器

使用`async with`管理异步资源：

```python
class AsyncDB:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()
```

### 异步迭代器

使用`async for`处理异步数据流：

```python
async def read_stream():
    async for chunk in stream_reader:
        process(chunk)
```

### 限制并发数

使用asyncio.Semaphore控制并发度：

```python
sem = asyncio.Semaphore(10)

async def limited_fetch(url):
    async with sem:
        return await fetch_data(url)
```

## 常见陷阱与最佳实践

### 避免阻塞事件循环

在协程中使用同步阻塞调用会阻塞整个事件循环。

**错误示例：**
```python
async def bad():
    time.sleep(1)  # 阻塞整个事件循环！
```

**正确做法：**
```python
async def good():
    await asyncio.sleep(1)  # 非阻塞
    # 或使用线程池执行阻塞操作
    result = await asyncio.to_thread(sync_function)
```

### 线程安全

大部分asyncio对象不是线程安全的，跨线程调用需要使用`loop.call_soon_threadsafe`。

### 调试异步代码

- 启用`PYTHONASYNCIODEBUG=1`环境变量
- 使用`asyncio.run(main(), debug=True)`
- 设置`loop.slow_callback_duration`检测慢回调

异步编程能显著提升IO密集型应用的性能，但需要理解其底层机制才能编写出正确高效的代码。

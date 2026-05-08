---
title: "Python 入门教程：从零到写出第一个程序"
description: "零基础 Python 编程入门，30 分钟掌握变量、条件、循环、函数等核心语法，手写第一个可运行程序。"
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/tech/python-tutorial.html
---

# Python 入门教程：从零到写出第一个程序

Python 是最适合初学者的编程语言——语法接近自然语言，生态强大到几乎无所不能。这篇教程带你 30 分钟入门。

## 安装 Python

macOS 自带 Python 3，终端输入 `python3 --version` 检查。Windows 去 python.org 下载安装包，安装时勾选 "Add Python to PATH"。

## 第一个程序
    
    
    print("Hello, World!")

保存为 `hello.py`，终端运行 `python3 hello.py`，看到输出就成功了。

## 变量和数据类型
    
    
    name = "小明"        # 字符串
    age = 25             # 整数
    height = 1.75        # 浮点数
    is_student = True    # 布尔值
    
    print(f"{name}今年{age}岁")

## 条件判断
    
    
    score = 85
    if score >= 90:
        print("优秀")
    elif score >= 60:
        print("及格")
    else:
        print("不及格")

## 循环
    
    
    # for 循环
    for i in range(5):
        print(f"第{i+1}次")
    
    # while 循环
    count = 0
    while count < 3:
        print(f"count = {count}")
        count += 1

## 列表和字典
    
    
    # 列表 — 有序集合
    fruits = ["苹果", "香蕉", "橘子"]
    fruits.append("葡萄")
    print(fruits[0])  # 苹果
    
    # 字典 — 键值对
    user = {"name": "小明", "age": 25, "city": "北京"}
    print(user["name"])  # 小明

## 函数
    
    
    def greet(name):
        return f"你好，{name}！"
    
    print(greet("小明"))  # 你好，小明！

## 下一步学什么

  1. **pip 包管理** — 安装第三方库
  2. **文件读写** — 处理文本和 CSV
  3. **requests 库** — 爬取网页和调用 API
  4. **Flask** — 写一个简单的 Web 应用

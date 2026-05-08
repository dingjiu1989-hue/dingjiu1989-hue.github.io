---
title: "单元测试入门：从零到写出第一个可维护的测试"
description: "零基础单元测试入门教程，覆盖 Python/pytest 实战，AAA 模式、Mock、Fixture 核心概念一网打尽。"
date: 2026-05-07
board: tech
url: https://dingjiu1989-hue.github.io/tech/unit-testing-guide.html
---

# 单元测试入门：从零到写出第一个可维护的测试

写单元测试是你从"会写代码"到"专业开发者"的分水岭。这篇文章用最少的理论带你直接上手。

## 为什么必须写测试

  * **重构有底气** — 有测试覆盖的代码，改完跑一次就知道有没有破坏现有功能
  * **文档即测试** — 测试描述了函数在各种输入下应该如何表现，比注释更可靠
  * **减少回归 Bug** — 修一个 Bug 加一个测试，同样的错不会再犯第二次



## AAA 模式（Arrange-Act-Assert）
    
    
    def test_add_two_numbers():
        # Arrange（准备）
        a, b = 2, 3
        # Act（执行）
        result = add(a, b)
        # Assert（断言）
        assert result == 5

## 第一个真实测试
    
    
    # user_service.py
    def get_full_name(user):
        return f"{user.first_name} {user.last_name}"
    
    # test_user_service.py
    def test_get_full_name():
        user = type('User', (), {'first_name': '张', 'last_name': '三'})()
        assert get_full_name(user) == "张 三"
    
    def test_get_full_name_empty_last():
        user = type('User', (), {'first_name': '李', 'last_name': ''})()
        assert get_full_name(user) == "李 "

## Mock 和 Fixture
    
    
    # Fixture: 共享的测试数据
    @pytest.fixture
    def sample_user():
        return User(id=1, name="张三", email="zhang@test.com")
    
    def test_user_email(sample_user):
        assert sample_user.email == "zhang@test.com"
    
    # Mock: 隔离外部依赖
    @patch("requests.get")
    def test_fetch_user(mock_get):
        mock_get.return_value.json.return_value = {"name": "张三"}
        result = fetch_user(1)
        assert result["name"] == "张三"

## 什么该测、什么不该测

  * **该测** — 业务逻辑、边界条件、错误路径、数据转换
  * **不该测** — 简单的 getter/setter、框架代码、第三方库的内部行为



## 起步建议

不用追求 100% 覆盖率——那会增加大量维护负担。先给核心业务逻辑写测试，看到覆盖率数字攀升的成就感会推着你继续写。

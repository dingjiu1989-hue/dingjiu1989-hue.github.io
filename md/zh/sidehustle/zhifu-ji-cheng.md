---
title: "Stripe集成指南：订阅、发票、退款、多币种处理"
description: "全面讲解Stripe支付集成的工程实践，涵盖订阅管理、定期发票生成、退款处理和跨境多币种收款的完整实现方案。"
date: 2026-05-12
board: sidehustle
url: https://dingjiu1989-hue.github.io/zh/sidehustle/zhifu-ji-cheng.html
---

## Stripe支付体系

Stripe是全球最流行的在线支付平台之一，尤其适合SaaS产品的支付需求。其API设计优雅，文档完善，支持订阅管理、发票和退款等全流程支付功能。

## 基础集成

### 支付流程

```python
import stripe
stripe.api_key = "sk_test_..."

# 1. 创建支付Intent
intent = stripe.PaymentIntent.create(
    amount=2000,  # 单位：分
    currency="usd",
    customer=customer_id,
)

# 2. 返回client_secret给前端
# 前端使用Stripe Elements完成支付确认
```

### 前端集成

使用Stripe提供的预构建UI组件，避免处理敏感的支付信息：

```javascript
import { Elements, PaymentElement } from '@stripe/react-stripe-js';

function CheckoutForm() {
  return (
    <form onSubmit={handleSubmit}>
      <PaymentElement />
      <button>支付</button>
    </form>
  );
}
```

## 订阅管理

订阅是SaaS产品的核心支付模式。

### 创建订阅

```python
# 创建价格
price = stripe.Price.create(
    product="prod_xxx",
    unit_amount=1999,  # $19.99
    currency="usd",
    recurring={"interval": "month"},
)

# 创建订阅
subscription = stripe.Subscription.create(
    customer=customer_id,
    items=[{"price": price.id}],
    trial_period_days=14,  # 14天免费试用
)
```

### 订阅状态管理

订阅的生命周期包括：trialing、active、past_due、canceled、incomplete。

需通过Webhook监听订阅状态变更：

```python
# Webhook处理
@app.post("/stripe/webhook")
async def stripe_webhook(payload: bytes, sig: str):
    event = stripe.Webhook.construct_event(payload, sig, webhook_secret)

    if event.type == "customer.subscription.updated":
        subscription = event.data.object
        # 更新数据库中的订阅状态
    elif event.type == "invoice.payment_succeeded":
        # 处理成功付款
    elif event.type == "invoice.payment_failed":
        # 处理付款失败（发送提醒邮件）
```

## 发票功能

Stripe Invoice支持自动生成和发送发票。

```python
# 创建发票
invoice = stripe.Invoice.create(
    customer=customer_id,
    auto_advance=True,  # 自动发送
    collection_method="charge_automatically",
    days_until_due=30,
)

# 手动添加费用项
stripe.InvoiceItem.create(
    customer=customer_id,
    amount=5000,
    currency="usd",
    description="额外存储服务",
    invoice=invoice.id,
)

# 发送发票
stripe.Invoice.send_invoice(invoice.id)
```

## 退款处理

```python
# 全额退款
stripe.Refund.create(
    payment_intent=pi_id,
)

# 部分退款
stripe.Refund.create(
    payment_intent=pi_id,
    amount=1000,
)
```

## 多币种处理

### 币种支持

Stripe支持135+种货币。处理多币种时注意：

1. 货币金额单位：大部分货币使用最小单位（分），但日元等零货币单位不同
2. 币种转换：Stripe自动处理货币转换，汇率每日更新
3. 结算货币：商家可以选择接收结算的货币

### 价格配置

```python
# 多币种价格
prices = {
    "usd": stripe.Price.create(product=prod.id, unit_amount=1999, currency="usd"),
    "eur": stripe.Price.create(product=prod.id, unit_amount=1899, currency="eur"),
    "cny": stripe.Price.create(product=prod.id, unit_amount=12900, currency="cny"),
}
```

Stripe作为支付基础设施，能够处理从简单到复杂的各类支付场景，是SaaS产品国际化的首选支付方案。

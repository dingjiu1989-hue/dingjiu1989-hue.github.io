---
title: "Web性能优化指南"
description: "全面覆盖前端性能优化策略，包括加载优化、渲染性能、资源压缩、缓存策略以及性能监控等核心实践方法。"
date: 2026-05-11
board: zh/tech
url: https://dingjiu1989-hue.github.io/zh/tech/web-performance.html
---

## 性能指标与测量

Web性能优化前先确定衡量标准。Core Web Vitals是Google推荐的核心指标：LCP（最大内容绘制）衡量加载性能，目标小于2.5秒；FID（首次输入延迟）衡量交互性，目标小于100毫秒；CLS（累积布局偏移）衡量视觉稳定性，目标小于0.1。

使用Lighthouse进行性能审计，获取具体优化建议。Web Vitals库可以在生产环境采集真实用户数据，帮助发现实际体验问题。

## 资源加载优化

**图片优化**：图片通常是页面体积的最大贡献者。使用WebP或AVIF格式替代传统JPEG/PNG，可以节省30-50%体积。实现响应式图片：`<img srcset="small.jpg 400w, medium.jpg 800w" sizes="(max-width: 600px) 400px, 800px">`。懒加载使用`loading="lazy"`属性，首屏以下图片延迟加载。

**代码分割**：使用Webpack或Vite的动态导入功能，将代码拆分为多个chunk。路由级别的代码分割确保首屏只加载需要的JS。配合Preload和Prefetch策略，提前加载关键资源和预测用户即将访问的页面。

## 渲染性能优化

避免渲染阻塞：将关键CSS内联在`<head>`中，非关键CSS异步加载。JavaScript使用defer或async属性，或移到底部加载。对于长时间任务，使用requestIdleCallback分解执行。

**虚拟列表**：渲染大量列表项时使用虚拟滚动技术。只渲染可视区域内的元素，滚动时动态替换内容。React中使用react-window或react-virtuoso库实现。

## 缓存策略

合理利用HTTP缓存大幅提升二次访问速度。静态资源使用强缓存：`Cache-Control: public, max-age=31536000, immutable`，配合文件名哈希实现更新。HTML文档使用协商缓存：`Cache-Control: no-cache`配合ETag验证。

Service Worker实现离线缓存和资源预缓存。使用Workbox库简化Service Worker的编写，配置预缓存策略让关键资源在安装阶段即完成缓存。

## 网络优化

启用HTTP/2或HTTP/3协议，支持多路复用减少连接数。配置CDN加速静态资源分发，将内容缓存到离用户最近的节点。使用资源提示（Resource Hints）：dns-prefetch、preconnect预建连接，preload预加载关键资源。

使用Brotli压缩算法替代gzip，压缩率可提升20-30%。在Nginx中配置：`brotli on; brotli_types text/html text/css application/javascript;`。

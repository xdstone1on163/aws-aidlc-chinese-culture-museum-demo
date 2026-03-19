# 非遗博物馆 - 需求澄清问题

在分析您的回答后，我发现了一些需要进一步确认的地方。请在 `[Answer]:` 后填写您的选择。

---

## Clarification 1: 功能复杂度 vs 项目规模

您选择了较高复杂度的功能（虚拟展厅/3D 展示、全球 CDN、智能推荐、混合数据库），但项目初期规模为小型（<100 非遗项目，<1000 日活）。请确认您的开发策略：

A) MVP 优先：先实现核心功能（图文视频展示、评价、论坛），虚拟展厅/3D、智能推荐等作为后续迭代
B) 一步到位：初期就实现所有功能，包括虚拟展厅/3D 展示和智能推荐
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Clarification 2: 虚拟展厅/3D 展示的具体需求

您选择了虚拟展厅/3D 展示，请确认具体期望：

A) 简单的 360° 全景图浏览（类似 Google Street View）
B) 基于 WebGL/Three.js 的 3D 虚拟展厅（用户可在虚拟空间中行走浏览）
C) 3D 模型展示（非遗物品的 3D 模型可旋转查看）
D) 以上全部
E) Other (please describe after [Answer]: tag below)

[Answer]: E先不做虚拟展厅/3D功能

---

## Clarification 3: 面向全球用户但仅邮箱登录

项目定位面向全世界用户，但认证方式仅选择了邮箱+密码。请确认：

A) 确认仅邮箱+密码，后续可扩展其他方式
B) 希望增加 Google/Facebook 等国际社交账号登录
C) Other (please describe after [Answer]: tag below)

[Answer]: A

---

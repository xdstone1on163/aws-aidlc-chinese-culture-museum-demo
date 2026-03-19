# 非遗博物馆 - Unit of Work 计划

## 分解策略

本项目采用**模块化单体架构**（Django 单项目 + Next.js 前端），所有后端模块在同一进程内运行，前后端分离部署。

基于架构特点，系统分解为以下开发单元：

| 单元 | 名称 | 范围 | 优先级 |
|------|------|------|--------|
| Unit 1 | 后端核心与认证 | core + accounts + Django 项目骨架 + Docker 基础设施 | MVP |
| Unit 2 | 媒体管理 | media（文件上传、存储、元数据） | MVP |
| Unit 3 | 非遗内容管理 | heritage + Django Admin 配置 | MVP |
| Unit 4 | 评价与搜索 | reviews + search (Elasticsearch) | MVP |
| Unit 5 | 前端应用 | Next.js 全部前端模块 (FE-01 ~ FE-05, FE-07) | MVP |
| Unit 6 | 社区论坛 | forum (后端 + 前端 FE-06) | P1 |

---

## 计划步骤

- [x] 1. 确认分解策略和单元划分（Q1=B media独立, Q2=A 前端整体, Q3=A 后端先行）
- [x] 2. 生成 `unit-of-work.md`（单元定义和职责）
- [x] 3. 生成 `unit-of-work-dependency.md`（单元依赖矩阵）
- [x] 4. 生成 `unit-of-work-story-map.md`（故事到单元的映射）
- [x] 5. 验证单元边界和依赖关系
- [x] 6. 确保所有故事已分配到单元（28/28 ✅）

---

## 分解决策问题

请回答以下问题，帮助确认单元分解方案。

## Question 1
上述 5 个开发单元的划分是否合理？Unit 1（核心+认证）作为第一个开发单元，为后续单元提供基础。

A) 合理，按此方案执行
B) 需要调整，将 media 从 Unit 2 独立为单独单元
C) 需要调整，将前端拆分为多个单元（如展示模块和用户模块分开）
D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2
Unit 4（前端应用）包含所有 MVP 前端模块。考虑到前端模块之间耦合较紧（共享布局、路由、状态），建议作为一个整体单元开发。你的看法？

A) 同意，前端作为一个整体单元
B) 拆分为两个单元：公共+展示 和 用户交互（评价、收藏、个人中心）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
开发顺序建议为 Unit 1 → Unit 2 → Unit 3 → Unit 4 → Unit 5（后端先行，前端在后端 API 就绪后开发）。是否同意？

A) 同意，后端先行策略
B) 希望前后端并行开发（Unit 1 完成后，Unit 2/3 和 Unit 4 同时进行）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

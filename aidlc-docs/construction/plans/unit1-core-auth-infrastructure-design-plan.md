# Unit 1: 后端核心与认证 - Infrastructure Design 计划

## 设计范围
将逻辑组件映射到本地 Docker Compose 基础设施，定义部署架构。

---

## 设计步骤

- [x] 1. 确认基础设施细节（Q1=A 宿主机运行Django, Q2=A named volume持久化）
- [x] 2. 生成 `infrastructure-design.md`（Docker Compose 服务定义、端口映射、数据卷）
- [x] 3. 生成 `deployment-architecture.md`（本地开发启动流程、环境变量、健康检查）
- [x] 4. 验证基础设施覆盖所有组件需求

---

## 基础设施问题

## Question 1
Django 开发服务器运行方式：后端是直接在宿主机运行（方便调试），还是也放在 Docker 容器中？

A) 宿主机运行 Django（方便调试和热重载），只有 PostgreSQL/Redis/ES 在 Docker 中
B) 全部服务都在 Docker 中运行（docker-compose up 一键启动全部）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
PostgreSQL 数据持久化：Docker 容器重启后数据是否保留？

A) 使用 Docker named volume 持久化（推荐，数据不丢失）
B) 不持久化，每次重启是干净数据库（开发测试用）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

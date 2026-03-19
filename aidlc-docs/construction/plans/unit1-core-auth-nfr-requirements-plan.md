# Unit 1: 后端核心与认证 - NFR Requirements 计划

## 评估范围
基于 Unit 1 的功能设计（用户认证、RBAC、JWT Token、Redis 锁定/黑名单），评估非功能需求并确定技术栈细节。

---

## 评估步骤

- [x] 1. 收集 NFR 决策信息（Q1=A 500ms, Q2=B Django4.2LTS, Q3=A CONN_MAX_AGE, Q4=B 纯文本日志, Q5=A pytest 80%）
- [x] 2. 生成 `nfr-requirements.md`（性能、安全、可用性、可维护性需求）
- [x] 3. 生成 `tech-stack-decisions.md`（技术栈版本和配置决策）
- [x] 4. 验证 NFR 需求与功能设计一致

---

## NFR 决策问题

## Question 1
API 响应时间目标：认证相关接口（登录、注册、Token 刷新）的响应时间要求？

A) ≤ 500ms（标准 Web 应用，MVP 推荐）
B) ≤ 200ms（高性能要求）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
Python 和 Django 版本选择：

A) Python 3.12 + Django 5.1 + DRF 3.15（最新稳定版）
B) Python 3.11 + Django 4.2 LTS + DRF 3.14（长期支持版，更保守）
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3
数据库连接池策略：Django 默认每次请求新建数据库连接。是否使用连接池？

A) 使用 Django 内置 CONN_MAX_AGE 持久连接（简单，MVP 够用）
B) 使用 django-db-connection-pool（第三方连接池，更高性能）
C) 不使用连接池，保持默认（最简单）
D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4
日志策略：开发和调试阶段的日志级别和输出方式？

A) 开发环境 DEBUG 级别输出到 console，结构化 JSON 格式（方便后续扩展）
B) 开发环境 DEBUG 级别输出到 console，纯文本格式（简单直观）
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 5
测试策略：Unit 1 的测试覆盖要求？

A) pytest + factory_boy，核心业务逻辑覆盖率 ≥ 80%
B) Django 内置 TestCase，关键流程测试即可，不设覆盖率目标
C) Other (please describe after [Answer]: tag below)

[Answer]: A

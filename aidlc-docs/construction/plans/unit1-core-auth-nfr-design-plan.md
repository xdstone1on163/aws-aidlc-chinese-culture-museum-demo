# Unit 1: 后端核心与认证 - NFR Design 计划

## 设计范围
将 NFR 需求转化为具体的设计模式和逻辑组件，指导 Unit 1 的代码实现。

---

## 设计步骤

- [x] 1. 确认设计模式选择（Q1=B DRF内置异常, Q2=A python-dotenv）
- [x] 2. 生成 `nfr-design-patterns.md`（安全、性能、可靠性设计模式）
- [x] 3. 生成 `logical-components.md`（中间件、工具类、配置组件）
- [x] 4. 验证设计模式覆盖所有 NFR 需求

---

## 设计决策问题

## Question 1
异常处理策略：DRF 提供了全局异常处理机制。如何组织自定义异常？

A) 统一异常处理器 + 自定义业务异常类层次结构（BusinessException → AuthException, ValidationException 等）
B) 直接使用 DRF 内置异常（APIException, ValidationError 等），不自定义
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2
配置管理：环境变量和敏感配置（数据库密码、SECRET_KEY）的管理方式？

A) python-dotenv + .env 文件（开发环境简单直接）
B) django-environ（功能更丰富，支持类型转换）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

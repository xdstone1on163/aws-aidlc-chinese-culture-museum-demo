# Unit 1: 后端核心与认证 - Functional Design 计划

## 单元范围
- core app：公共工具函数、分页器、权限类、异常处理、中间件
- accounts app：用户注册、登录、JWT Token、密码重置、邮箱验证、RBAC
- Django 项目骨架、Docker Compose 基础设施配置

## 关联故事
- US-U01 注册账号 [MVP]
- US-U02 登录账号 [MVP]
- US-U03 重置密码 [MVP]
- US-A01 管理用户账号 [MVP]
- US-A02 分配用户角色 [MVP]

---

## 设计步骤

- [x] 1. 确认业务逻辑细节（Q1=A硬编码角色, Q2=A console email, Q3=B宽松Token, Q4=A Redis计数器, Q5=A Redis黑名单）
- [x] 2. 生成 `domain-entities.md`（领域实体：User、Role、Permission 模型定义）
- [x] 3. 生成 `business-rules.md`（业务规则：密码策略、登录锁定、Token 管理、RBAC 规则）
- [x] 4. 生成 `business-logic-model.md`（业务流程：注册流程、登录流程、密码重置流程、角色管理流程）
- [x] 5. 验证设计覆盖所有关联故事的验收标准

---

## 业务逻辑问题

## Question 1
用户角色体系设计：需求中定义了三种角色（注册用户、内容管理员、系统管理员）。角色权限是硬编码在代码中，还是通过数据库动态配置？

A) 硬编码三种固定角色，权限在代码中定义（简单直接，MVP 推荐）
B) 数据库动态角色+权限配置，支持自定义角色（灵活但复杂）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
邮箱验证流程：注册后需要邮箱验证激活账号。开发环境中如何处理邮件发送？

A) 开发环境使用 Django console email backend（邮件内容输出到终端），生产环境再配置 SMTP
B) 直接配置一个真实的 SMTP 服务（如 Gmail SMTP）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
JWT Token 策略：Access Token 和 Refresh Token 的有效期如何设置？

A) Access Token 30分钟 + Refresh Token 7天（标准配置）
B) Access Token 1小时 + Refresh Token 30天（宽松配置，减少用户重新登录频率）
C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4
账号锁定策略：US-U02 要求连续5次登录失败后锁定15分钟。锁定机制如何实现？

A) 基于 Redis 计数器（内存中记录失败次数，自动过期）
B) 基于数据库字段（User 模型增加 failed_attempts 和 locked_until 字段）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
用户禁用处理：US-A01 要求禁用用户后"已登录会话立即失效"。如何实现 Token 失效？

A) Redis Token 黑名单（禁用时将用户所有 Token 加入黑名单）
B) 数据库 is_active 字段 + 每次请求校验用户状态（简单但每次多一次 DB 查询）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

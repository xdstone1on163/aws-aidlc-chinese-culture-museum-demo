# Unit 1: 后端核心与认证 - NFR 设计模式

## 1. 安全模式

### 1.1 JWT 认证模式
- **模式**: Stateless Token Authentication
- **实现**: djangorestframework-simplejwt
- **流程**: 登录签发 Access+Refresh Token → 请求携带 Access Token → 过期后用 Refresh Token 刷新
- **配置**: Access 1h / Refresh 7~30d（根据 remember_me）

### 1.2 Redis Token 黑名单模式
- **模式**: Token Revocation via Blacklist
- **触发**: 用户被禁用、密码重置
- **实现**: Redis SET `user_disabled:{user_id}` with TTL
- **校验**: JWT 认证中间件在 Token 验证后检查黑名单

### 1.3 登录防暴力破解模式
- **模式**: Rate Limiting + Account Lockout
- **实现**: Redis INCR `login_fail:{email}` with TTL 15min
- **阈值**: 5 次失败 → 锁定 15 分钟
- **重置**: 登录成功后 DEL key

### 1.4 API 速率限制模式
- **模式**: Token Bucket (DRF Throttling)
- **后端**: Redis
- **策略**: 匿名 60/min, 认证 120/min, 登录 10/min

### 1.5 RBAC 权限模式
- **模式**: Role-Based Access Control (硬编码)
- **实现**: DRF Permission Classes
- **角色**: user / content_manager / admin
- **校验**: 自定义 Permission 类检查 request.user.role

---

## 2. 性能模式

### 2.1 数据库连接复用
- **模式**: Persistent Connection
- **实现**: Django `CONN_MAX_AGE = 600`
- **效果**: 避免每次请求建连开销

### 2.2 Redis 缓存模式
- **模式**: Cache-Aside
- **实现**: django-redis 作为 Django cache backend
- **用途**: 速率限制计数、登录锁定、Token 黑名单
- **策略**: 认证相关数据不缓存（实时性要求高），仅用 Redis 做计数和黑名单

---

## 3. 可靠性模式

### 3.1 优雅降级
- **场景**: Redis 不可用
- **策略**: 登录锁定和黑名单功能降级（捕获 Redis 连接异常，允许请求通过）
- **实现**: try/except 包裹 Redis 操作，异常时记录日志并跳过

### 3.2 统一错误响应
- **模式**: Global Exception Handler
- **实现**: DRF `EXCEPTION_HANDLER` 自定义（基于内置异常类，不自定义异常层次）
- **格式**: 统一 `{ code, message, errors }` 响应结构
- **覆盖**: 400/401/403/404/429/500 等所有 HTTP 错误码

---

## 4. 可维护性模式

### 4.1 环境配置分离
- **模式**: Environment-Specific Configuration
- **实现**: python-dotenv + .env 文件 + settings 分层（base/dev/test）
- **敏感数据**: SECRET_KEY、DB 密码、Redis URL 从 .env 读取

### 4.2 模块边界模式
- **模式**: Service Layer Pattern
- **实现**: 每个 app 暴露 `services.py`，其他 app 只通过 service 函数交互
- **约束**: 禁止跨 app 直接导入 models

### 4.3 日志模式
- **模式**: Structured Logging
- **实现**: Django logging framework，纯文本输出到 console
- **级别**: 开发环境 DEBUG，关键操作（登录、角色变更、禁用）记录 INFO 级别

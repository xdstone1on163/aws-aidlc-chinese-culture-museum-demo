# Unit 1: 后端核心与认证 - 逻辑组件

## 组件清单

```
apps/core/                         apps/accounts/
├── response.py [LC-01]            ├── authentication.py [LC-05]
├── permissions.py [LC-02]         ├── throttles.py [LC-06]
├── pagination.py [LC-03]          ├── services.py [LC-07]
├── exceptions.py [LC-04]          └── signals.py [LC-08]
└── middleware.py [LC-09]
```

---

## LC-01: 统一响应格式 (core/response.py)

**职责**: 包装所有 API 响应为统一格式

**输出格式**:
```json
// 成功
{ "code": 200, "message": "success", "data": { ... } }

// 错误
{ "code": 400, "message": "错误描述", "errors": { "field": ["详情"] } }
```

**实现**: 自定义 DRF Response renderer 或 response wrapper 函数

---

## LC-02: 权限类 (core/permissions.py)

**职责**: RBAC 权限校验

**组件**:
- `IsAdmin` — 仅 admin 角色可访问
- `IsContentManager` — content_manager 或 admin 可访问
- `IsAuthenticated` — 已登录用户（DRF 内置，复用）
- `IsVerified` — 已验证邮箱的用户

**使用方式**: DRF ViewSet 的 `permission_classes` 属性

---

## LC-03: 分页器 (core/pagination.py)

**职责**: 统一分页配置

**配置**:
- 默认每页 12 条（列表页）
- 管理页每页 20 条
- 最大每页 100 条
- 基于 DRF `PageNumberPagination`

---

## LC-04: 全局异常处理 (core/exceptions.py)

**职责**: 统一异常响应格式

**实现**: 自定义 `custom_exception_handler` 函数，注册到 DRF `EXCEPTION_HANDLER`
- 捕获 DRF 内置异常（ValidationError, AuthenticationFailed, PermissionDenied, NotFound, Throttled）
- 转换为统一 `{ code, message, errors }` 格式
- 未知异常返回 500 + 通用错误信息（不暴露内部细节）

---

## LC-05: JWT 认证 + 黑名单校验 (accounts/authentication.py)

**职责**: 扩展 simplejwt 认证，增加 Redis 黑名单检查

**流程**:
1. 调用 simplejwt 验证 Token 签名和有效期
2. 提取 user_id
3. 检查 Redis `user_disabled:{user_id}` 是否存在
4. 存在 → 抛出 AuthenticationFailed
5. 不存在 → 返回 user 对象

**降级**: Redis 不可用时跳过黑名单检查，记录 WARNING 日志

---

## LC-06: 登录速率限制 (accounts/throttles.py)

**职责**: 登录接口专用速率限制

**实现**: 继承 DRF `SimpleRateThrottle`
- scope = 'login'
- rate = '10/min'
- 以 email 为 key（而非 IP，防止同一邮箱被不同 IP 暴力破解）

---

## LC-07: 认证服务层 (accounts/services.py)

**职责**: 认证业务逻辑封装，供其他 app 调用

**对外接口**:
- `get_user_by_id(user_id) → User`
- `check_permission(user, permission) → bool`
- `get_user_role(user_id) → str`

**内部方法**:
- `register_user(email, password, nickname) → User`
- `verify_email(token) → bool`
- `login_user(email, password, remember_me) → TokenPair`
- `check_login_lockout(email) → bool`
- `record_login_failure(email) → int`
- `clear_login_failures(email) → None`
- `request_password_reset(email) → None`
- `reset_password(token, new_password) → bool`
- `disable_user(user_id) → None`
- `enable_user(user_id) → None`
- `change_user_role(user_id, new_role, admin_user) → None`

---

## LC-08: 用户信号 (accounts/signals.py)

**职责**: 发送用户相关事件

**信号**:
- `user_deactivated(sender, user)` — 用户被禁用时发送，供 reviews/forum 模块监听

---

## LC-09: 请求日志中间件 (core/middleware.py)

**职责**: 记录 API 请求日志

**记录内容**: 请求方法、路径、用户ID、响应状态码、耗时
**级别**: INFO（正常请求）、WARNING（4xx）、ERROR（5xx）

---

## 组件依赖关系

```
LC-04 (异常处理) ← 所有 View 使用
LC-01 (响应格式) ← 所有 View 使用
LC-02 (权限类)   ← 所有需要权限的 View 使用
LC-03 (分页器)   ← 所有列表 View 使用
LC-05 (JWT认证)  ← DRF 全局认证配置
LC-06 (速率限制) ← 登录 View 使用
LC-07 (服务层)   ← accounts View + 其他 app 调用
LC-08 (信号)     ← reviews/forum app 监听
LC-09 (中间件)   ← Django 全局中间件
```

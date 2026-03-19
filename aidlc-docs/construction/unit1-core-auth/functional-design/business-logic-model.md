# Unit 1: 后端核心与认证 - 业务流程模型

## 1. 用户注册流程

```
用户提交注册表单 (email, password, confirm_password, nickname)
  │
  ├─ 校验 email 格式 → 失败 → 返回格式错误
  ├─ 校验 email 唯一性 → 已存在 → 返回"该邮箱已注册"
  ├─ 校验 nickname 唯一性 → 已存在 → 返回"该昵称已被使用"
  ├─ 校验 password == confirm_password → 不一致 → 返回错误
  ├─ 校验密码强度 (≥8位, 含字母+数字) → 不满足 → 返回错误
  │
  ├─ 创建 User (role=user, is_active=True, is_verified=False)
  ├─ 创建 UserProfile (nickname, language=zh)
  ├─ 生成 EmailVerificationToken (expires_at = now + 24h)
  ├─ 发送验证邮件 (开发环境: console backend)
  │
  └─ 返回 201 + 用户基本信息 + "请查收验证邮件"
```

---

## 2. 邮箱验证流程

```
用户点击验证链接 (/api/accounts/verify-email/?token=xxx)
  │
  ├─ 查找 Token → 不存在 → 返回"无效的验证链接"
  ├─ 检查 is_used → 已使用 → 返回"链接已使用"
  ├─ 检查 expires_at → 已过期 → 返回"链接已过期，请重新发送"
  │
  ├─ 设置 user.is_verified = True
  ├─ 设置 token.is_used = True
  │
  └─ 返回 200 + "邮箱验证成功"
```

---

## 3. 用户登录流程

```
用户提交登录表单 (email, password, remember_me)
  │
  ├─ 检查 Redis login_fail:{email} ≥ 5 → 是 → 返回"账号已锁定，请15分钟后重试"
  │
  ├─ 查找 User by email → 不存在 → INCR 计数器 → 返回"邮箱或密码错误"
  ├─ 检查 user.is_active → False → 返回"账号已被禁用"
  ├─ 验证密码 → 错误 → INCR 计数器 → 返回"邮箱或密码错误"
  │
  ├─ DEL login_fail:{email} (清除失败计数)
  ├─ 更新 user.last_login
  ├─ 签发 Access Token (1小时)
  ├─ 签发 Refresh Token (remember_me ? 30天 : 7天)
  │
  └─ 返回 200 + { access, refresh, user_info }
      user_info: { id, email, nickname, role, is_verified, avatar }
```

---

## 4. Token 刷新流程

```
客户端提交 Refresh Token
  │
  ├─ 验证 Token 签名和有效期 → 无效 → 返回 401
  ├─ 检查 Redis user_disabled:{user_id} → 存在 → 返回 401 "账号已被禁用"
  │
  ├─ 签发新 Access Token
  │
  └─ 返回 200 + { access }
```

---

## 5. 密码重置流程

```
步骤一：请求重置
用户提交邮箱 (email)
  │
  ├─ 查找 User by email
  ├─ 无论是否找到 → 返回"如果该邮箱已注册，将收到重置邮件"
  │
  ├─ [如果找到] 生成 PasswordResetToken (expires_at = now + 24h)
  ├─ [如果找到] 发送重置邮件 (含重置链接)
  │
  └─ 返回 200

步骤二：执行重置
用户提交 (token, new_password, confirm_password)
  │
  ├─ 查找 Token → 不存在 → 返回"无效的重置链接"
  ├─ 检查 is_used → 已使用 → 返回"链接已使用"
  ├─ 检查 expires_at → 已过期 → 返回"链接已过期"
  ├─ 校验 new_password == confirm_password
  ├─ 校验密码强度
  │
  ├─ 更新 user.password
  ├─ 设置 token.is_used = True
  ├─ 将 user_id 加入 Redis 黑名单 (使旧 Token 失效)
  │
  └─ 返回 200 + "密码重置成功，请重新登录"
```

---

## 6. 用户管理流程（Admin）

### 6.1 查看用户列表
```
Admin 请求用户列表 (filters: role, is_active; search: nickname/email)
  │
  ├─ 校验请求者 role == admin → 否 → 返回 403
  ├─ 查询 User + UserProfile (JOIN)
  ├─ 应用筛选和搜索条件
  ├─ 分页 (默认20条/页)
  │
  └─ 返回 200 + 用户列表
```

### 6.2 禁用/启用用户
```
Admin 提交 (user_id, is_active)
  │
  ├─ 校验请求者 role == admin → 否 → 返回 403
  ├─ 查找目标 User → 不存在 → 返回 404
  │
  ├─ [禁用] 设置 user.is_active = False
  │         SET Redis user_disabled:{user_id} = 1, TTL = 1小时
  │
  ├─ [启用] 设置 user.is_active = True
  │         DEL Redis user_disabled:{user_id}
  │
  ├─ 记录 Django Admin LogEntry
  │
  └─ 返回 200
```

### 6.3 分配角色
```
Admin 提交 (user_id, new_role)
  │
  ├─ 校验请求者 role == admin → 否 → 返回 403
  ├─ 校验 user_id != 请求者 ID → 相同 → 返回"不能修改自己的角色"
  ├─ 校验 new_role 在 [user, content_manager, admin] 中
  ├─ 查找目标 User → 不存在 → 返回 404
  │
  ├─ 更新 user.role = new_role
  ├─ 记录 Django Admin LogEntry
  │
  └─ 返回 200
```

---

## 7. JWT 认证中间件流程

```
每个 API 请求
  │
  ├─ 提取 Authorization: Bearer {token}
  ├─ 无 Token → 匿名用户（仅允许公开接口）
  │
  ├─ 验证 Token 签名和有效期 → 无效 → 返回 401
  ├─ 提取 user_id
  ├─ 检查 Redis user_disabled:{user_id} → 存在 → 返回 401
  │
  └─ 设置 request.user = User 对象
```

---

## 故事验收标准覆盖验证

| 故事 | 验收标准 | 覆盖状态 |
|------|----------|----------|
| US-U01 | 注册表单字段、密码强度、验证邮件、邮箱重复提示、实时校验 | ✅ 全部覆盖 |
| US-U02 | 登录表单、跳转、错误提示、记住我、5次锁定 | ✅ 全部覆盖 |
| US-U03 | 忘记密码链接、发送邮件、24h有效期、跳转、防枚举 | ✅ 全部覆盖 |
| US-A01 | 用户列表、筛选搜索、禁用启用、会话失效 | ✅ 全部覆盖 |
| US-A02 | 角色分配、三种角色、立即生效、不能改自己、操作日志 | ✅ 全部覆盖 |

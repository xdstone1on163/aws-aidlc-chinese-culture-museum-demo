# Unit 1: 后端核心与认证 - 领域实体

## 实体关系图

```
┌──────────────┐       ┌──────────────┐
│     User     │──1:1──│  UserProfile │
│              │       │              │
│ id (PK)      │       │ user (FK)    │
│ email (UQ)   │       │ nickname(UQ) │
│ password     │       │ avatar       │
│ role         │       │ bio          │
│ is_active    │       │ language     │
│ is_verified  │       └──────────────┘
│ date_joined  │
└──────────────┘
```

---

## User（用户）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, auto | 主键 |
| email | EmailField | UNIQUE, NOT NULL | 登录邮箱 |
| password | CharField | NOT NULL | 哈希密码（Django 内置） |
| role | CharField | NOT NULL, default='user' | 角色：user / content_manager / admin |
| is_active | BooleanField | default=True | 账号是否启用 |
| is_verified | BooleanField | default=False | 邮箱是否已验证 |
| date_joined | DateTimeField | auto_now_add | 注册时间 |
| last_login | DateTimeField | nullable | 最后登录时间 |

**说明**：
- 继承 `AbstractBaseUser` + `PermissionsMixin`，用 email 替代 username 作为登录标识
- role 字段使用 CharField + choices，硬编码三种角色

### 角色枚举

```python
class UserRole:
    USER = 'user'                    # 注册用户
    CONTENT_MANAGER = 'content_manager'  # 内容管理员
    ADMIN = 'admin'                  # 系统管理员

    CHOICES = [
        (USER, '注册用户'),
        (CONTENT_MANAGER, '内容管理员'),
        (ADMIN, '系统管理员'),
    ]
```

### 角色权限映射（硬编码）

| 权限 | user | content_manager | admin |
|------|------|-----------------|-------|
| 浏览非遗项目 | ✅ | ✅ | ✅ |
| 评分评论 | ✅ | ✅ | ✅ |
| 收藏项目 | ✅ | ✅ | ✅ |
| 管理个人资料 | ✅ | ✅ | ✅ |
| 创建/编辑非遗项目 | ❌ | ✅ | ✅ |
| 管理多媒体资源 | ❌ | ✅ | ✅ |
| 管理评论 | ❌ | ✅ | ✅ |
| 管理用户账号 | ❌ | ❌ | ✅ |
| 分配角色 | ❌ | ❌ | ✅ |
| 系统配置 | ❌ | ❌ | ✅ |

---

## UserProfile（用户资料）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, auto | 主键 |
| user | OneToOneField(User) | UNIQUE, CASCADE | 关联用户 |
| nickname | CharField(50) | UNIQUE, NOT NULL | 昵称 |
| avatar | CharField(255) | nullable | 头像文件路径 |
| bio | TextField | nullable, max 200字 | 个人简介 |
| language | CharField(5) | default='zh' | 语言偏好：zh / en |
| created_at | DateTimeField | auto_now_add | 创建时间 |
| updated_at | DateTimeField | auto_now | 更新时间 |

**说明**：
- 与 User 一对一关联，注册时自动创建
- nickname 全局唯一，用于前端展示

---

## EmailVerificationToken（邮箱验证令牌）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, auto | 主键 |
| user | ForeignKey(User) | CASCADE | 关联用户 |
| token | CharField(64) | UNIQUE | 验证令牌（随机生成） |
| created_at | DateTimeField | auto_now_add | 创建时间 |
| expires_at | DateTimeField | NOT NULL | 过期时间（创建后24小时） |
| is_used | BooleanField | default=False | 是否已使用 |

---

## PasswordResetToken（密码重置令牌）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, auto | 主键 |
| user | ForeignKey(User) | CASCADE | 关联用户 |
| token | CharField(64) | UNIQUE | 重置令牌 |
| created_at | DateTimeField | auto_now_add | 创建时间 |
| expires_at | DateTimeField | NOT NULL | 过期时间（创建后24小时） |
| is_used | BooleanField | default=False | 是否已使用 |

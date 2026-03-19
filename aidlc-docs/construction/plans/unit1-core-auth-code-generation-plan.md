# Unit 1: 后端核心与认证 - Code Generation 计划

## 单元上下文

### 实现故事
- US-U01 注册账号 [MVP]
- US-U02 登录账号 [MVP]
- US-U03 重置密码 [MVP]
- US-A01 管理用户账号 [MVP]
- US-A02 分配用户角色 [MVP]

### 依赖
- 无外部单元依赖（第一个单元）
- 基础设施依赖：PostgreSQL、Redis（Docker Compose）

### 交付范围
- Django 项目骨架 + 配置
- Docker Compose 基础设施
- core app（公共模块）
- accounts app（认证模块）
- 单元测试
- API 文档配置

---

## 代码生成步骤

### 项目骨架与基础设施
- [ ] Step 1: Django 项目骨架（config/ 目录、settings 分层、manage.py）
- [x] Step 1: Django 项目骨架（config/ 目录、settings 分层、manage.py）
- [x] Step 2: 依赖文件（requirements/base.txt、dev.txt、test.txt）
- [x] Step 3: Docker Compose + .env.example
- [x] Step 4: 开发工具配置（pytest.ini、ruff.toml、.gitignore）

### core app（公共模块）
- [x] Step 5: core app 初始化 + response.py（统一响应格式）
- [x] Step 6: core/permissions.py（RBAC 权限类）+ core/pagination.py（分页器）
- [x] Step 7: core/exceptions.py（全局异常处理）+ core/middleware.py（请求日志）

### accounts app（认证模块）- Models & Services
- [x] Step 8: accounts/models.py（User、UserProfile、EmailVerificationToken、PasswordResetToken）
- [x] Step 9: accounts/services.py（认证服务层：注册、登录、锁定、重置、禁用、角色管理）
- [x] Step 10: accounts/authentication.py（JWT + Redis 黑名单认证）+ accounts/throttles.py（登录限流）

### accounts app（认证模块）- API Layer
- [x] Step 11: accounts/serializers.py（请求/响应序列化器）
- [x] Step 12: accounts/views.py（API 视图：注册、登录、Token刷新、密码重置、用户管理）
- [x] Step 13: accounts/urls.py + config/urls.py（路由配置）+ accounts/admin.py（Django Admin）

### 测试
- [x] Step 14: accounts/tests/factories.py（测试数据工厂）
- [x] Step 15: accounts/tests/test_models.py（模型测试）
- [x] Step 16: accounts/tests/test_services.py（服务层测试：注册、登录、锁定、重置、禁用）
- [x] Step 17: accounts/tests/test_views.py（API 端点测试）

### 文档与部署
- [x] Step 18: API 文档配置（drf-spectacular）+ 健康检查端点
- [x] Step 19: README.md（项目说明、启动指南）
- [ ] Step 15: accounts/tests/test_models.py（模型测试）
- [ ] Step 16: accounts/tests/test_services.py（服务层测试：注册、登录、锁定、重置、禁用）
- [ ] Step 17: accounts/tests/test_views.py（API 端点测试）

### 文档与部署
- [ ] Step 18: API 文档配置（drf-spectacular）+ 健康检查端点
- [ ] Step 19: README.md（项目说明、启动指南）

---

## 故事到步骤映射

| 故事 | 覆盖步骤 |
|------|----------|
| US-U01 注册账号 | Step 8-9 (models+services), Step 11-13 (API), Step 15-17 (tests) |
| US-U02 登录账号 | Step 9-10 (services+auth+throttle), Step 11-13 (API), Step 16-17 (tests) |
| US-U03 重置密码 | Step 8-9 (models+services), Step 11-13 (API), Step 16-17 (tests) |
| US-A01 管理用户账号 | Step 8-9 (models+services), Step 12-13 (views+admin), Step 17 (tests) |
| US-A02 分配用户角色 | Step 6 (permissions), Step 9 (services), Step 12-13 (views), Step 17 (tests) |

# Unit 1: 后端核心与认证 - 非功能需求

## NFR-01: 性能

| 指标 | 目标 | 说明 |
|------|------|------|
| API 响应时间 | ≤ 500ms (P95) | 登录、注册、Token 刷新等认证接口 |
| 数据库查询 | ≤ 100ms | 单次 ORM 查询 |
| Redis 操作 | ≤ 10ms | 锁定计数、黑名单检查 |
| 密码哈希 | ≤ 300ms | PBKDF2 哈希计算（Django 默认） |

### 数据库连接
- 使用 `CONN_MAX_AGE = 600`（10分钟持久连接）
- 开发环境足够，避免频繁建连开销

---

## NFR-02: 安全

| 需求 | 实现方式 |
|------|----------|
| 密码存储 | Django PBKDF2-SHA256 哈希（内置） |
| 传输安全 | 开发环境 HTTP，生产环境 HTTPS（反向代理） |
| JWT 签名 | HS256 算法 + SECRET_KEY |
| CSRF 防护 | DRF 默认豁免（Token 认证），Django Admin 保留 CSRF |
| CORS | django-cors-headers，开发环境允许 localhost:3000 |
| 速率限制 | DRF throttling + Redis 后端 |
| 防暴力破解 | Redis 登录失败计数器（5次/15分钟锁定） |
| Token 黑名单 | Redis 存储被禁用用户 ID |
| 密码重置防枚举 | 无论邮箱是否存在，返回相同响应 |
| SQL 注入 | Django ORM 参数化查询（内置防护） |
| XSS | DRF JSON 响应（无 HTML 渲染风险） |

---

## NFR-03: 可用性

| 需求 | 目标 |
|------|------|
| 本地开发可用性 | Docker Compose 一键启动所有服务 |
| 服务依赖 | PostgreSQL、Redis 不可用时返回明确错误 |
| 优雅降级 | Redis 不可用时，登录锁定和黑名单功能降级（允许登录但不锁定） |

---

## NFR-04: 可维护性

| 需求 | 实现方式 |
|------|----------|
| 代码规范 | PEP 8 + flake8/ruff 检查 |
| 类型提示 | Python type hints（关键函数） |
| 日志 | Django logging，DEBUG 级别，纯文本输出到 console |
| 测试 | pytest + factory_boy，核心业务逻辑覆盖率 ≥ 80% |
| 文档 | API 接口使用 DRF 自动生成文档（drf-spectacular） |
| 数据库迁移 | Django migrations，每次模型变更生成迁移文件 |

---

## NFR-05: 可扩展性

| 需求 | 设计策略 |
|------|----------|
| 存储切换 | Django STORAGES 抽象层，未来可切换 S3 |
| 邮件服务 | Django email backend 抽象，开发用 console，生产切换 SMTP |
| 缓存 | Django cache framework + Redis，统一缓存接口 |
| 模块边界 | App 间通过 services.py 通信，不直接导入 models |

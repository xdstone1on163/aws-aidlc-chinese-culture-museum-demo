# Unit 1: 后端核心与认证 - 技术栈决策

## 核心技术栈

| 技术 | 版本 | 选择理由 |
|------|------|----------|
| Python | 3.11 | LTS 支持，生态成熟稳定 |
| Django | 4.2 LTS | 长期支持版（至 2026-04），安全补丁保障 |
| Django REST Framework | 3.14 | 与 Django 4.2 兼容的稳定版本 |
| PostgreSQL | 15 | 当前 LTS 版本，Docker 官方镜像 |
| Redis | 7 | 最新稳定版，Docker 官方镜像 |

## Python 依赖包

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| django | 4.2.* | Web 框架 |
| djangorestframework | 3.14.* | REST API 框架 |
| djangorestframework-simplejwt | 5.3.* | JWT 认证 |
| django-cors-headers | 4.3.* | CORS 跨域支持 |
| django-redis | 5.4.* | Redis 缓存/会话后端 |
| redis | 5.0.* | Redis Python 客户端 |
| psycopg2-binary | 2.9.* | PostgreSQL 驱动 |
| drf-spectacular | 0.27.* | OpenAPI 文档生成 |
| python-dotenv | 1.0.* | 环境变量管理 |

### 开发/测试依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| pytest | 8.* | 测试框架 |
| pytest-django | 4.8.* | Django 测试集成 |
| pytest-cov | 5.* | 覆盖率报告 |
| factory-boy | 3.3.* | 测试数据工厂 |
| faker | 28.* | 假数据生成 |
| ruff | 0.5.* | 代码检查和格式化 |

## Docker 配置

### docker-compose.yml 服务

| 服务 | 镜像 | 端口 | 说明 |
|------|------|------|------|
| db | postgres:15-alpine | 5432 | 主数据库 |
| redis | redis:7-alpine | 6379 | 缓存/会话/锁定 |
| elasticsearch | elasticsearch:8.11.0 | 9200 | 全文搜索（Unit 4 使用，此处预配置） |

### Django 关键配置

```python
# settings.py 关键配置项

# 数据库连接池
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'CONN_MAX_AGE': 600,  # 10分钟持久连接
    }
}

# JWT 配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ALGORITHM': 'HS256',
}

# Redis 缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
    }
}

# 邮件（开发环境）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 日志（纯文本）
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'level': 'DEBUG', 'handlers': ['console']},
}

# 速率限制
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/min',
        'user': '120/min',
        'login': '10/min',
    }
}
```

## 项目结构（Unit 1 范围）

```
ich_museum/                    # Django 项目根目录
├── manage.py
├── requirements/
│   ├── base.txt              # 核心依赖
│   ├── dev.txt               # 开发依赖
│   └── test.txt              # 测试依赖
├── config/                    # Django 项目配置
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py           # 公共配置
│   │   ├── dev.py            # 开发环境
│   │   └── test.py           # 测试环境
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/                  # 公共模块
│   │   ├── pagination.py
│   │   ├── permissions.py
│   │   ├── exceptions.py
│   │   ├── middleware.py
│   │   └── response.py
│   └── accounts/              # 认证模块
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── services.py
│       ├── admin.py
│       └── tests/
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── pytest.ini
└── ruff.toml
```

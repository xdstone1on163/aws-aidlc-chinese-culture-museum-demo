# Unit 1: 后端核心与认证 - 部署架构

## 本地开发环境启动流程

### 首次启动

```bash
# 1. 启动基础设施服务
docker-compose up -d

# 2. 创建 Python 虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements/dev.txt

# 4. 复制环境变量
cp .env.example .env

# 5. 数据库迁移
python manage.py migrate

# 6. 创建超级管理员
python manage.py createsuperuser

# 7. 启动开发服务器
python manage.py runserver
```

### 日常启动

```bash
# 1. 启动 Docker 服务（如果未运行）
docker-compose up -d

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 启动 Django
python manage.py runserver
```

### 停止服务

```bash
# 停止 Docker 服务（保留数据）
docker-compose stop

# 停止并删除容器（保留数据卷）
docker-compose down

# 停止并删除所有数据（慎用）
docker-compose down -v
```

---

## 环境变量 (.env)

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_SETTINGS_MODULE=config.settings.dev
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=ich_museum
DB_USER=ich_user
DB_PASSWORD=ich_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Elasticsearch
ELASTICSEARCH_URL=http://localhost:9200

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email (dev: console backend)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Media
MEDIA_ROOT=media/
MEDIA_URL=/media/
```

---

## 健康检查

| 服务 | 检查方式 | 间隔 |
|------|----------|------|
| PostgreSQL | `pg_isready` | 10s |
| Redis | `redis-cli ping` | 10s |
| Elasticsearch | `curl /_cluster/health` | 15s |
| Django | `GET /api/health/` | 手动 |

### Django 健康检查端点

```
GET /api/health/

Response:
{
  "status": "ok",
  "services": {
    "database": "ok",
    "redis": "ok",
    "elasticsearch": "ok"
  }
}
```

---

## 开发工具命令

```bash
# 运行测试
pytest

# 运行测试（带覆盖率）
pytest --cov=apps --cov-report=html

# 代码检查
ruff check apps/

# 代码格式化
ruff format apps/

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# Django Admin
http://localhost:8000/admin/

# API 文档
http://localhost:8000/api/docs/
```

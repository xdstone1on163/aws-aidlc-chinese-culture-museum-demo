# 非遗博物馆 (ICH Museum)

中国非物质文化遗产展示平台后端服务。

## 技术栈

- Python 3.11 + Django 4.2 LTS + DRF 3.14
- PostgreSQL 15 + Redis 7 + Elasticsearch 8.11
- JWT 认证 (simplejwt)

## 快速启动

### 前置条件
- Python 3.11+
- Docker (Colima / Docker Desktop)

### 1. 启动基础设施
```bash
docker-compose up -d
```

### 2. 创建虚拟环境
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
```

### 3. 配置环境变量
```bash
cp .env.example .env
```

### 4. 数据库迁移
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. 启动开发服务器
```bash
python manage.py runserver
```

## 访问地址

| 服务 | 地址 |
|------|------|
| API | http://localhost:8000/api/ |
| API 文档 | http://localhost:8000/api/docs/ |
| Django Admin | http://localhost:8000/admin/ |
| 健康检查 | http://localhost:8000/api/health/ |

## 测试

```bash
pip install -r requirements/test.txt
pytest
pytest --cov=apps --cov-report=html
```

## 代码检查

```bash
ruff check apps/
ruff format apps/
```

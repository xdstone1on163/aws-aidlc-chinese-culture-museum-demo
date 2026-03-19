# Unit 1: 后端核心与认证 - 基础设施设计

## 部署架构概览

```
┌─────────────────────────────────────────────────┐
│                  宿主机 (macOS)                   │
│                                                   │
│  ┌─────────────────┐   ┌──────────────────────┐  │
│  │ Django Dev Server│   │ Next.js Dev Server   │  │
│  │ localhost:8000   │   │ localhost:3000       │  │
│  │ (python manage.py│   │ (npm run dev)        │  │
│  │  runserver)      │   │ [Unit 5]             │  │
│  └────────┬────────┘   └──────────────────────┘  │
│            │                                       │
│  ┌─────────▼───────────────────────────────────┐  │
│  │           Docker Compose                     │  │
│  │                                              │  │
│  │  ┌──────────┐ ┌────────┐ ┌───────────────┐  │  │
│  │  │PostgreSQL│ │ Redis  │ │ Elasticsearch │  │  │
│  │  │  :5432   │ │ :6379  │ │    :9200      │  │  │
│  │  │ (volume) │ │(volume)│ │   (volume)    │  │  │
│  │  └──────────┘ └────────┘ └───────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  media/  ← Django FileSystemStorage                 │
└─────────────────────────────────────────────────────┘
```

---

## Docker Compose 服务定义

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: ich_museum_db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ich_museum
      POSTGRES_USER: ich_user
      POSTGRES_PASSWORD: ich_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ich_user -d ich_museum"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: ich_museum_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  elasticsearch:
    image: elasticsearch:8.11.0
    container_name: ich_museum_es
    ports:
      - "9200:9200"
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 5

volumes:
  postgres_data:
  redis_data:
  es_data:
```

---

## 端口映射

| 服务 | 容器端口 | 宿主机端口 | 说明 |
|------|----------|------------|------|
| PostgreSQL | 5432 | 5432 | 主数据库 |
| Redis | 6379 | 6379 | 缓存/会话/锁定 |
| Elasticsearch | 9200 | 9200 | 全文搜索（Unit 4 使用） |
| Django | - | 8000 | 宿主机直接运行 |
| Next.js | - | 3000 | 宿主机直接运行（Unit 5） |

---

## 数据卷

| 卷名 | 挂载路径 | 用途 |
|------|----------|------|
| postgres_data | /var/lib/postgresql/data | PostgreSQL 数据持久化 |
| redis_data | /data | Redis 数据持久化 |
| es_data | /usr/share/elasticsearch/data | Elasticsearch 索引持久化 |

---

## 逻辑组件到基础设施映射

| 逻辑组件 | 基础设施 | 说明 |
|----------|----------|------|
| Django App (core, accounts) | 宿主机 Python 3.11 | 直接运行，方便调试 |
| PostgreSQL 数据库 | Docker postgres:15-alpine | named volume 持久化 |
| Redis 缓存/锁定/黑名单 | Docker redis:7-alpine | named volume 持久化 |
| Elasticsearch 搜索 | Docker elasticsearch:8.11.0 | 单节点模式，安全关闭 |
| 文件存储 | 宿主机 media/ 目录 | Django FileSystemStorage |
| 邮件服务 | Django console backend | 开发环境输出到终端 |

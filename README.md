# 非遗博物馆 (ICH Museum)

中国非物质文化遗产展示平台 — Intangible Cultural Heritage Museum

## 技术栈

### 后端 (`ich_museum/`)
- Python 3.11+ / Django 4.2 LTS / Django REST Framework 3.14
- PostgreSQL 15 / Redis 7 / Elasticsearch 8.11
- JWT 认证 (SimpleJWT) / drf-spectacular (OpenAPI 文档)

### 前端 (`ich_museum_frontend/`)
- Next.js 14 (App Router) / React 18 / TypeScript 5.4
- Tailwind CSS 3.4 / next-intl (中英双语)

## 项目结构

```
├── ich_museum/                  # Django 后端
│   ├── config/                  # Django 配置 (settings/urls/wsgi)
│   ├── apps/
│   │   ├── core/                # 共享工具：统一响应格式、异常处理、分页、中间件
│   │   ├── accounts/            # 用户认证：邮箱注册、JWT、角色权限、登录锁定
│   │   ├── heritage/            # 非遗项目：CRUD、分类、地域、传承人、收藏
│   │   ├── media/               # 媒体文件：通用附件管理
│   │   ├── reviews/             # 评论系统：评分、嵌套回复、软删除
│   │   └── search/              # 搜索服务：Elasticsearch 全文检索
│   ├── requirements/            # 依赖管理 (base/dev/test)
│   └── docker-compose.yml       # 基础设施 (PostgreSQL/Redis/ES)
├── ich_museum_frontend/         # Next.js 前端
│   ├── src/
│   │   ├── app/[locale]/        # 页面路由 (中英双语)
│   │   ├── components/          # React 组件
│   │   ├── contexts/            # Auth Context
│   │   ├── lib/                 # API 客户端、类型定义
│   │   └── i18n/                # 国际化配置
│   └── messages/                # 翻译文件 (zh.json/en.json)
└── aidlc-docs/                  # AI-DLC 设计文档
    ├── inception/               # 需求、用户故事、应用设计
    └── construction/            # 功能设计、NFR、基础设施、构建指南
```

## 快速启动

### 前置条件

| 工具 | 版本 |
|------|------|
| Python | 3.11+ |
| Node.js | 18+ |
| Docker | 20+ (Colima 或 Docker Desktop) |

### 1. 启动基础设施

```bash
# 如果使用 Colima
colima start

cd ich_museum
docker-compose up -d
# 等待所有服务 healthy（约 30 秒）
docker-compose ps
```

### 2. 后端设置

```bash
cd ich_museum
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/test.txt
cp .env.example .env
python manage.py makemigrations accounts media heritage reviews
python manage.py migrate
python manage.py loaddata apps/heritage/fixtures/categories.json
python manage.py createsuperuser
python manage.py load_sample_data    # 加载 13 个示例非遗项目
```

### 3. 启动后端

```bash
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

### 4. 前端设置与启动（另开终端）

```bash
cd ich_museum_frontend
npm install
npm run dev
```

### 5. 初始化搜索索引

```bash
cd ich_museum
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py shell -c "
from apps.search.services import ensure_index, sync_item_index
from apps.heritage.models import HeritageItem
ensure_index()
for item in HeritageItem.objects.filter(status='published'):
    sync_item_index(item.id)
"
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| API 文档 (Swagger) | http://localhost:8000/api/docs/ |
| 管理后台 | http://localhost:8000/admin/ |
| 健康检查 | http://localhost:8000/api/health/ |

## 测试

```bash
cd ich_museum
source venv/bin/activate
pytest                                    # 运行所有测试
pytest apps/accounts/tests/test_views.py  # 单个文件
pytest -k test_login_user                 # 单个测试
pytest --cov=apps --cov-report=html       # 覆盖率报告
```

## 代码检查

```bash
# 后端
cd ich_museum
ruff check apps/
ruff format apps/

# 前端
cd ich_museum_frontend
npm run lint
```

## 架构说明

- **Service Layer 模式**：业务逻辑在 `services.py`，视图层只做序列化和路由
- **跨 app 通信**：通过 `services.py` 中的公开函数，不直接导入其他 app 的 model
- **统一 API 响应格式**：`{"code": 200, "message": "success", "data": {...}}`
- **Django Signal + ES 同步**：非遗项目保存/删除时通过 signal 自动同步到 Elasticsearch
- **角色权限**：user（普通用户）/ content_manager（内容管理员）/ admin（系统管理员）

## AI-DLC 工作流

本项目使用 AI-DLC (AI Development Lifecycle) 工作流开发，设计文档位于 `aidlc-docs/` 目录，涵盖从需求分析到代码生成的完整过程。

# 构建与测试总结

## 项目概览

| 项目 | 技术栈 | 目录 |
|------|--------|------|
| 后端 | Python 3.11 + Django 4.2 LTS + DRF 3.14 | `ich_museum/` |
| 前端 | Next.js 14 + React 18 + TypeScript + Tailwind | `ich_museum_frontend/` |
| 基础设施 | Docker Compose (PostgreSQL 15 + Redis 7 + ES 8.11) | `ich_museum/docker-compose.yml` |

## 后端模块

| 模块 | 功能 | 模型数 | API 端点数 | 测试用例数 |
|------|------|--------|------------|------------|
| core | 公共工具（响应/权限/分页/异常/中间件） | 0 | 1 (health) | 0 |
| accounts | 认证、RBAC、JWT | 4 | 10 | 26 |
| media | 文件上传、存储管理 | 1 | 6 | 5 |
| heritage | 非遗项目 CRUD、收藏 | 5 | 10 | 6 |
| reviews | 评分、评论、回复 | 1 | 4 | 7 |
| search | Elasticsearch 全文搜索 | 0 | 1 | 0 |
| **合计** | | **11** | **32** | **44** |

## 前端页面

| 页面 | 路由 | 功能 |
|------|------|------|
| 首页 | `/[locale]/` | 非遗项目列表 + 分类筛选 |
| 项目详情 | `/[locale]/heritage/[id]` | Markdown 渲染 + 收藏 + 评论 |
| 搜索 | `/[locale]/search` | 关键词搜索 |
| 登录 | `/[locale]/login` | 邮箱密码登录 |
| 注册 | `/[locale]/register` | 用户注册 |
| 个人中心 | `/[locale]/profile` | 资料编辑 |
| 收藏夹 | `/[locale]/favorites` | 收藏列表 |

## 测试策略

| 测试类型 | 状态 | 说明 |
|----------|------|------|
| 单元测试 | ✅ 已生成 | pytest + factory_boy，44 个用例 |
| 集成测试 | ✅ 指南已生成 | 5 个端到端场景（手动 curl） |
| 性能测试 | ✅ 指南已生成 | MVP 阶段辅助参考 |
| 代码质量 | ✅ 工具已配置 | ruff check + format |

## 快速启动命令

```bash
# 后端
cd ich_museum
docker-compose up -d
source venv/bin/activate
pip install -r requirements/test.txt
cp .env.example .env
python manage.py migrate
python manage.py loaddata apps/heritage/fixtures/categories.json
python manage.py createsuperuser
python manage.py runserver

# 前端（另一个终端）
cd ich_museum_frontend
npm install
npm run dev

# 测试
cd ich_museum
pytest --cov=apps
ruff check apps/
```

## MVP 交付状态

| 故事 | 状态 |
|------|------|
| 21 个 MVP 故事 (Unit 1-5) | ✅ 已实现 |
| 6 个 P1 故事 (含 Unit 6 论坛) | ⏳ 待后续迭代 |
| 1 个 P2 故事 | ⏳ 远期规划 |

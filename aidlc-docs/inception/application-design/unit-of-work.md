# 非遗博物馆 - 工作单元定义

## 概览

| 单元 | 名称 | 范围 | 优先级 | 开发顺序 |
|------|------|------|--------|----------|
| Unit 1 | 后端核心与认证 | core + accounts + Django 项目骨架 + Docker 基础设施 | MVP | 1st |
| Unit 2 | 媒体管理 | media（文件上传、存储、元数据管理） | MVP | 2nd |
| Unit 3 | 非遗内容管理 | heritage + Django Admin 配置 | MVP | 3rd |
| Unit 4 | 评价与搜索 | reviews + search (Elasticsearch) | MVP | 4th |
| Unit 5 | 前端应用 | Next.js 全部 MVP 前端模块 | MVP | 5th |
| Unit 6 | 社区论坛 | forum 后端 + 前端 FE-06 | P1 | 6th |

---

## Unit 1: 后端核心与认证

### 职责
- Django 项目初始化（settings、urls、wsgi）
- Docker Compose 配置（PostgreSQL、Elasticsearch、Redis）
- core app：公共工具函数、分页器、权限类、异常处理、中间件
- accounts app：用户注册、登录、JWT Token、密码重置、邮箱验证、RBAC

### 包含组件
- BE-07 core
- BE-01 accounts
- DL-01 PostgreSQL（Docker 配置）
- DL-04 Redis（Docker 配置）

### 交付物
- Django 项目骨架（settings、requirements、Dockerfile）
- docker-compose.yml（PostgreSQL、Redis、Elasticsearch）
- core app（分页、权限、异常处理）
- accounts app（models、serializers、views、urls、services）
- JWT 认证配置（djangorestframework-simplejwt）
- Django Admin 基础配置

### 前置条件
- 无（第一个单元）

---

## Unit 2: 媒体管理

### 职责
- media app：文件上传处理（multipart/form-data）
- 文件类型/大小校验
- 本地文件存储管理（Django FileSystemStorage）
- 媒体元数据 CRUD
- STORAGES 配置（为未来 S3 切换预留接口）

### 包含组件
- BE-05 media
- DL-03 本地文件存储

### 交付物
- media app（models、serializers、views、urls、services）
- 文件上传校验逻辑（类型、大小限制）
- Django STORAGES 配置
- MEDIA_ROOT / MEDIA_URL 配置

### 前置条件
- Unit 1（core 公共模块、accounts 认证）

---

## Unit 3: 非遗内容管理

### 职责
- heritage app：非遗项目 CRUD、分类管理、状态管理（草稿/发布/下架）
- 收藏功能
- Django Admin 后台管理界面配置
- Django Signals 发送（heritage_item_saved / deleted）

### 包含组件
- BE-02 heritage

### 交付物
- heritage app（models、serializers、views、urls、services）
- Django Admin 配置（HeritageItem、Category、Region、Inheritor 管理界面）
- 收藏功能 API
- Signal 定义（供 search 模块监听）

### 前置条件
- Unit 1（core、accounts）
- Unit 2（media 文件关联）

---

## Unit 4: 评价与搜索

### 职责
- reviews app：评分、评论 CRUD、评论管理、嵌套回复
- search app：Elasticsearch 索引管理、全文搜索、分类筛选
- Signal 接收（heritage_item_saved → 同步索引）

### 包含组件
- BE-03 reviews
- BE-06 search
- DL-02 Elasticsearch（索引配置）

### 交付物
- reviews app（models、serializers、views、urls、services）
- search app（Elasticsearch 索引定义、搜索查询、Signal handler）
- Elasticsearch 索引映射（中英文分词配置）

### 前置条件
- Unit 1（core、accounts）
- Unit 3（heritage 数据源）
- Unit 2（media，评论图片上传）

---

## Unit 5: 前端应用

### 职责
- Next.js 项目初始化（App Router、TypeScript）
- 公共布局（导航栏、页脚、语言切换）
- 国际化（中英双语）
- 非遗展示模块（列表、详情、画廊）
- 用户模块（注册、登录、个人中心、收藏）
- 评价模块（评分、评论列表、评论表单）
- 搜索模块（搜索框、结果页、筛选器）

### 包含组件
- FE-01 公共布局
- FE-02 非遗展示模块
- FE-03 用户模块
- FE-04 评价模块
- FE-05 搜索模块
- FE-07 国际化模块

### 交付物
- Next.js 项目骨架（App Router、TypeScript、Tailwind CSS）
- 公共布局组件和国际化配置
- 所有 MVP 页面和组件
- API 调用层（fetch wrapper、类型定义）
- React Context（认证状态管理）

### 前置条件
- Unit 1 ~ Unit 4（所有后端 API 就绪）

---

## Unit 6: 社区论坛 `[P1]`

### 职责
- forum app：论坛分区、帖子 CRUD、回复管理
- 前端论坛模块：分区列表、帖子列表、帖子详情、发帖/回帖

### 包含组件
- BE-04 forum
- FE-06 社区论坛模块

### 交付物
- forum app（models、serializers、views、urls、services）
- 前端论坛页面和组件
- Django Admin 论坛管理配置

### 前置条件
- Unit 1（core、accounts）
- Unit 5（前端框架已就绪）

# 构建指南

## 前置条件

| 工具 | 版本 | 说明 |
|------|------|------|
| Python | 3.11+ | 后端运行时 |
| Node.js | 18+ | 前端运行时 |
| Docker | 20+ | 基础设施服务（Colima 或 Docker Desktop） |
| docker-compose | 2.0+ | 服务编排 |

## 后端构建

### 1. 启动基础设施
```bash
cd ich_museum
docker-compose up -d
# 等待所有服务健康检查通过（约 30 秒）
docker-compose ps  # 确认 3 个服务都是 healthy
```

### 2. 创建 Python 虚拟环境
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements/test.txt
```

### 4. 配置环境变量
```bash
cp .env.example .env
# .env 默认值即可用于本地开发
```

### 5. 数据库迁移
```bash
python manage.py makemigrations accounts media heritage reviews
python manage.py migrate
```

### 6. 加载初始数据
```bash
python manage.py loaddata apps/heritage/fixtures/categories.json
```

### 7. 创建管理员账号
```bash
python manage.py createsuperuser
# 输入邮箱和密码
```

### 8. 验证后端启动
```bash
python manage.py runserver
# 访问 http://localhost:8000/api/health/ 确认服务正常
# 访问 http://localhost:8000/api/docs/ 查看 API 文档
# 访问 http://localhost:8000/admin/ 进入管理后台
```

## 前端构建

### 1. 安装依赖
```bash
cd ich_museum_frontend
npm install
```

### 2. 验证前端启动
```bash
npm run dev
# 访问 http://localhost:3000 确认页面正常
# API 请求通过 Next.js rewrites 代理到 localhost:8000
```

## 构建验证清单

- [ ] Docker 服务全部 healthy（PostgreSQL, Redis, Elasticsearch）
- [ ] Django migrate 无错误
- [ ] Django runserver 启动成功
- [ ] /api/health/ 返回所有服务 ok
- [ ] /api/docs/ 显示 Swagger 文档
- [ ] /admin/ 可登录
- [ ] 前端 npm run dev 启动成功
- [ ] 前端首页可访问

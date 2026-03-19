# 系统启动指南

## 1. 启动基础设施

```bash
colima start
cd ich_museum
docker-compose up -d
```

## 2. 启动后端

```bash
cd ich_museum
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

## 3. 启动前端（另开终端）

```bash
cd ich_museum_frontend
npm run dev
```

## 访问地址

| 服务 | 地址 |
|------|------|
| 前端 | http://localhost:3000 |
| API 文档 | http://localhost:8000/api/docs/ |
| 管理后台 | http://localhost:8000/admin/ |
| 健康检查 | http://localhost:8000/api/health/ |

管理后台账号：admin@cgtv.com / Welcome1#

## 关闭系统

### 1. 停止前端和后端

在各自终端中按 `Ctrl+C`。

### 2. 停止基础设施

```bash
cd ich_museum
docker-compose down          # 停止容器（保留数据）
docker-compose down -v       # 停止容器并删除所有数据卷（PostgreSQL/Redis/ES 数据将丢失）
```

### 3. 停止 Colima（可选）

```bash
colima stop
```

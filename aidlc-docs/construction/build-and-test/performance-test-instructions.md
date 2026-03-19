# 性能测试指南

## 性能目标（NFR 定义）

| 指标 | 目标 |
|------|------|
| API 响应时间 (P95) | ≤ 500ms |
| 数据库查询 | ≤ 100ms |
| Redis 操作 | ≤ 10ms |

## 测试方法

### 基础性能验证（手动）

使用 Django Debug Toolbar 或 Django Silk 在开发环境验证：

```bash
# 安装 django-silk（可选）
pip install django-silk

# 在 settings/dev.py 中添加:
# INSTALLED_APPS += ['silk']
# MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
# 访问 http://localhost:8000/silk/ 查看请求性能
```

### API 响应时间测试
```bash
# 使用 curl 测量响应时间
curl -w "\nTotal: %{time_total}s\n" http://localhost:8000/api/heritage/items/
curl -w "\nTotal: %{time_total}s\n" http://localhost:8000/api/search/?q=京剧
curl -w "\nTotal: %{time_total}s\n" -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
```

### 并发测试（可选，使用 ab 或 wrk）
```bash
# Apache Bench - 100 请求，10 并发
ab -n 100 -c 10 http://localhost:8000/api/heritage/items/

# wrk - 30 秒压测
wrk -t4 -c50 -d30s http://localhost:8000/api/heritage/items/
```

## MVP 阶段说明
MVP 阶段以功能验证为主，性能测试为辅助参考。正式性能测试在生产环境部署前执行。

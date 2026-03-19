# 集成测试指南

## 测试环境准备
```bash
cd ich_museum
docker-compose up -d
source venv/bin/activate
python manage.py migrate
python manage.py loaddata apps/heritage/fixtures/categories.json
python manage.py runserver  # 在另一个终端
```

## 集成测试场景

### 场景 1: 用户注册 → 验证 → 登录完整流程
```bash
# 1. 注册
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","confirm_password":"testpass123","nickname":"testuser"}'
# 预期: 201, 终端输出验证邮件

# 2. 从终端复制验证 token，验证邮箱
curl "http://localhost:8000/api/accounts/verify-email/?token=<token>"
# 预期: 200, 邮箱验证成功

# 3. 登录
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'
# 预期: 200, 返回 access + refresh token
```

### 场景 2: 非遗项目创建 → 搜索索引同步
```bash
# 1. 用管理员 token 创建项目
curl -X POST http://localhost:8000/api/heritage/manage/items/create/ \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"京剧","category":4,"summary":"中国传统戏剧","description":"# 京剧\n\n京剧是中国五大戏曲剧种之一","status":"published"}'
# 预期: 201

# 2. 等待 1 秒（同步 ES 索引）
# 3. 搜索
curl "http://localhost:8000/api/search/?q=京剧"
# 预期: 200, results 包含刚创建的项目
```

### 场景 3: 评价 → 评分统计
```bash
# 1. 用普通用户 token 评价
curl -X POST http://localhost:8000/api/reviews/items/<item_id>/reviews/create/ \
  -H "Authorization: Bearer <user_token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"非常精彩","rating":5}'
# 预期: 201

# 2. 查看评分统计
curl "http://localhost:8000/api/reviews/items/<item_id>/rating/"
# 预期: 200, average_rating=5.0, review_count=1
```

### 场景 4: 收藏 → 取消收藏
```bash
# 1. 收藏
curl -X POST http://localhost:8000/api/heritage/items/<item_id>/favorite/ \
  -H "Authorization: Bearer <user_token>"
# 预期: 200, is_favorited=true

# 2. 再次调用（取消收藏）
curl -X POST http://localhost:8000/api/heritage/items/<item_id>/favorite/ \
  -H "Authorization: Bearer <user_token>"
# 预期: 200, is_favorited=false
```

### 场景 5: 前后端集成
```bash
# 启动前端: cd ich_museum_frontend && npm run dev
# 1. 访问 http://localhost:3000 → 首页显示非遗项目列表
# 2. 点击项目 → 详情页显示 Markdown 渲染内容
# 3. 注册/登录 → 可评价和收藏
# 4. 搜索 → 返回 ES 搜索结果
# 5. 切换语言 → 界面文本切换
```

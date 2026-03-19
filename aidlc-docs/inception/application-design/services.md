# 非遗博物馆 - 服务层设计

## 架构模式

**模块化单体**：Django 单项目，按 app 严格划分模块边界，模块间通过定义好的内部接口通信，为未来可能的微服务拆分做准备。

---

## 服务编排模式

### 原则
1. 每个 Django App 拥有独立的 models、serializers、views、urls
2. App 之间不直接导入对方的 models，通过 service 层函数交互
3. 每个 App 暴露 `services.py` 作为对外接口
4. 公共逻辑放在 `core` app 中

### 模块间通信方式
- **同步调用**: App 之间通过 service 层函数直接调用（进程内）
- **信号机制**: Django Signals 用于松耦合的事件通知（如：非遗项目更新 → 触发搜索索引同步）

---

## 服务定义

### AuthService（accounts app）
- **职责**: 用户认证、授权、Token 管理
- **对外接口**:
  - `get_user_by_id(user_id) → User`
  - `check_permission(user, permission) → bool`
  - `get_user_role(user_id) → Role`
- **被依赖方**: heritage, reviews, forum, media

### HeritageService（heritage app）
- **职责**: 非遗项目业务逻辑、收藏管理
- **对外接口**:
  - `get_item_by_id(item_id) → HeritageItem`
  - `get_item_summary(item_id) → dict`（供搜索索引使用）
  - `check_item_exists(item_id) → bool`
- **被依赖方**: reviews, search
- **依赖**: AuthService（权限校验）, MediaService（媒体关联）

### ReviewService（reviews app）
- **职责**: 评价业务逻辑、评分统计
- **对外接口**:
  - `get_rating_stats(item_id) → dict`（平均分、评价数）
- **依赖**: AuthService（用户信息）, HeritageService（项目关联）

### ForumService（forum app）`[P1]`
- **职责**: 论坛帖子和回复业务逻辑
- **对外接口**:
  - `get_user_post_count(user_id) → int`
- **依赖**: AuthService（用户信息）

### MediaService（media app）
- **职责**: 文件上传处理、本地文件存储管理
- **对外接口**:
  - `handle_upload(file, object_type, object_id) → MediaFile`
  - `get_media_by_object(object_type, object_id) → list[MediaFile]`
  - `delete_media_files(object_type, object_id) → None`
- **被依赖方**: heritage, reviews
- **外部依赖**: Django FileSystemStorage（通过 STORAGES 配置，未来可切换为 S3）

### SearchService（search app）
- **职责**: 搜索查询、索引管理
- **对外接口**:
  - `search_items(query, filters) → SearchResult`
  - `sync_item_index(item_id) → None`
- **依赖**: HeritageService（数据源）
- **外部依赖**: Elasticsearch Python Client

---

## Django Signals 事件

| 信号 | 发送方 | 接收方 | 触发时机 |
|------|--------|--------|----------|
| heritage_item_saved | heritage | search | 非遗项目创建/更新后 |
| heritage_item_deleted | heritage | search, media | 非遗项目删除后 |
| user_deactivated | accounts | reviews, forum | 用户被禁用后 |

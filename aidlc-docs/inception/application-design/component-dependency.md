# 非遗博物馆 - 组件依赖关系

## 依赖矩阵

| 组件 ↓ 依赖 → | core | accounts | heritage | reviews | forum | media | search |
|----------------|------|----------|----------|---------|-------|-------|--------|
| **core** | - | - | - | - | - | - | - |
| **accounts** | ✅ | - | - | - | - | - | - |
| **heritage** | ✅ | ✅ | - | - | - | ✅ | - |
| **reviews** | ✅ | ✅ | ✅ | - | - | ✅ | - |
| **forum** | ✅ | ✅ | - | - | - | - | - |
| **media** | ✅ | ✅ | - | - | - | - | - |
| **search** | ✅ | - | ✅ | - | - | - | - |

**说明**: ✅ 表示行组件依赖列组件的服务接口

---

## 数据流向图

```
用户浏览器
    │
    ├──→ Next.js 前端 ──→ REST API ──→ Django 后端
    │                                      │
    │                          ┌───────────┤
    │                          │           │
    │                    ┌─────▼─────┐  ┌──▼──────────┐
    │                    │PostgreSQL │  │Elasticsearch│
    │                    │(主数据)   │  │(搜索索引)   │
    │                    │ (Docker)  │  │ (Docker)    │
    │                    └───────────┘  └─────────────┘
    │                          │
    │                    ┌─────▼─────┐
    │                    │  Redis    │
    │                    │(缓存/会话)│
    │                    │ (Docker)  │
    │                    └───────────┘
    │
    └──→ Django MEDIA_ROOT (本地文件存储)
```

---

## 关键数据流

### 1. 非遗项目创建流程
```
内容管理员 → 前端表单 → heritage API (创建项目)
                     → media API (上传文件，multipart/form-data)
           → Django 后端存储文件到本地 MEDIA_ROOT
           → media API 返回文件元数据
           → heritage_item_saved 信号 → search (同步索引)
```

### 2. 搜索流程
```
用户 → 前端搜索框 → search API → Elasticsearch (查询)
                              → 返回匹配结果 ID 列表
                              → heritage service (补充详情)
                              → 返回完整搜索结果
```

### 3. 评价流程
```
注册用户 → 前端评价表单 → reviews API (创建评论)
                       → media API (图片上传到后端，如有)
                       → 返回评论数据
                       → 前端更新评论列表和评分统计
```

---

## 外部服务依赖

| 外部服务 | 使用方 | 用途 |
|----------|--------|------|
| PostgreSQL (Docker) | 所有后端模块 | 主数据库 |
| Elasticsearch (Docker) | search 模块 | 全文搜索引擎 |
| Redis (Docker) | 全局 | 缓存、会话、速率限制 |
| SMTP 邮件服务 | accounts 模块 | 注册验证、密码重置邮件（开发环境可用 console backend） |
| 本地文件系统 | media 模块 | 图片、视频、音频存储 |

## 本地开发环境说明

所有基础设施服务通过 Docker Compose 运行：
- PostgreSQL: 端口 5432
- Elasticsearch: 端口 9200
- Redis: 端口 6379
- 媒体文件存储在 Django 项目的 `media/` 目录下
- 未来迁移到云环境时，只需修改 Django STORAGES 和数据库连接配置

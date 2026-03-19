# Unit 3: 非遗内容管理 - 领域实体

## Category（分类）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | AutoField | PK | 主键 |
| name | CharField(50) | UNIQUE | 分类名称（中文） |
| name_en | CharField(100) | nullable | 英文名称 |
| code | CharField(20) | UNIQUE | 分类编码（如 folk_literature） |
| sort_order | IntegerField | default=0 | 排序 |

**预置十大类**：民间文学、传统音乐、传统舞蹈、传统戏剧、曲艺、传统体育/游艺/杂技、传统美术、传统技艺、传统医药、民俗

## Region（地域）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | AutoField | PK | 主键 |
| name | CharField(50) | UNIQUE | 地域名称 |
| name_en | CharField(100) | nullable | 英文名称 |

## Inheritor（传承人）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| name | CharField(100) | NOT NULL | 姓名 |
| name_en | CharField(200) | nullable | 英文名 |
| title | CharField(100) | nullable | 称号/级别 |
| bio | TextField | nullable | 简介 |
| bio_en | TextField | nullable | 英文简介 |

## HeritageItem（非遗项目）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| name | CharField(200) | NOT NULL | 项目名称 |
| name_en | CharField(400) | nullable | 英文名称 |
| category | FK(Category) | NOT NULL | 分类 |
| region | FK(Region) | nullable | 地域 |
| summary | TextField(500) | NOT NULL | 简介摘要 |
| summary_en | TextField(500) | nullable | 英文摘要 |
| description | TextField | NOT NULL | 详细描述（Markdown） |
| description_en | TextField | nullable | 英文描述（Markdown） |
| history | TextField | nullable | 历史背景 |
| history_en | TextField | nullable | 英文历史 |
| status | CharField(20) | default=draft | 状态：draft/published/archived |
| created_by | FK(User) | NOT NULL | 创建者 |
| created_at | DateTimeField | auto_now_add | 创建时间 |
| updated_at | DateTimeField | auto_now | 更新时间 |

## HeritageInheritor（项目-传承人关联）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| heritage_item | FK(HeritageItem) | CASCADE | 非遗项目 |
| inheritor | FK(Inheritor) | CASCADE | 传承人 |

## Favorite（收藏）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 主键 |
| user | FK(User) | CASCADE | 用户 |
| heritage_item | FK(HeritageItem) | CASCADE | 非遗项目 |
| created_at | DateTimeField | auto_now_add | 收藏时间 |

**约束**: (user, heritage_item) UNIQUE — 同一用户对同一项目只能收藏一次

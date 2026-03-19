# Unit 4: 评价与搜索 - Functional Design 计划

## 关联故事
- US-U04 对非遗项目评分和评论 [MVP]
- US-U08 在评论区讨论 [MVP]
- US-C05 管理用户评论 [MVP]
- US-G03 搜索非遗项目 [MVP]
- US-G05 查看非遗项目评价 [MVP]

---

## 设计问题

## Question 1
Elasticsearch 索引同步策略：heritage 项目创建/更新后如何同步到 ES？

A) 同步方式 — Signal handler 中直接调用 ES 客户端更新索引（简单直接，MVP 推荐）
B) 异步方式 — Signal handler 发送 Celery 任务异步更新（需要引入 Celery，更复杂）
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
评论嵌套回复：US-U08 要求"最多2层嵌套"。数据模型如何设计？

A) 自引用外键（parent_id 指向父评论），查询时限制嵌套深度为 2
B) 扁平存储 + reply_to 字段，前端负责嵌套展示
C) Other (please describe after [Answer]: tag below)

[Answer]: B

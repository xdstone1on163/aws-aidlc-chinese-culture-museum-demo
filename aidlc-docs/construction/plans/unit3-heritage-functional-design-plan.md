# Unit 3: 非遗内容管理 - Functional Design 计划

## 关联故事
- US-C01 创建非遗项目 [MVP]
- US-C02 编辑非遗项目 [MVP]
- US-C04 管理非遗项目列表 [MVP]
- US-U06 收藏非遗项目 [MVP]
- US-C06 录入双语内容 [P1]

---

## 设计问题

## Question 1
非遗项目的十大分类数据如何管理？需求中提到"按中国国家级非遗名录十大类筛选"。

A) 预置固定数据（通过 migration 或 fixture 导入十大类），不允许前端增删
B) 后台可管理的分类表（Django Admin 可增删改），初始数据通过 fixture 导入
C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 2
非遗项目的"详细描述"字段需要富文本编辑。后端如何存储？

A) 存储为 HTML 字符串（TextField），前端使用富文本编辑器（如 TipTap/Quill），后端做 XSS 过滤
B) 存储为 Markdown 文本，前端渲染为 HTML
C) Other (please describe after [Answer]: tag below)

[Answer]: B

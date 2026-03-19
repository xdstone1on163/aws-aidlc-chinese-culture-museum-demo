# Unit 3: 非遗内容管理 - 业务规则

## BR-H01: 项目状态管理
| 状态 | 说明 | 可见性 |
|------|------|--------|
| draft | 草稿 | 仅创建者和管理员可见 |
| published | 已发布 | 所有用户可见 |
| archived | 已下架 | 仅管理员可见 |

**状态转换**: draft → published, published → archived, archived → published

## BR-H02: 权限规则
| 操作 | 权限 |
|------|------|
| 浏览已发布项目 | 所有人（含匿名） |
| 创建/编辑项目 | content_manager, admin |
| 发布/下架项目 | content_manager, admin |
| 批量操作 | content_manager, admin |
| 收藏项目 | 已登录用户 |

## BR-H03: 分类规则
- 十大类通过 fixture 预置，不可通过 API 增删
- 每个项目必须属于一个分类
- Django Admin 中分类为只读

## BR-H04: 双语内容规则 [P1]
- 中文字段为必填，英文字段为选填
- 前端英文版：有英文内容显示英文，无则显示中文原文

## BR-H05: 收藏规则
- 同一用户对同一项目只能收藏一次
- 重复收藏返回已收藏状态（幂等）
- 取消收藏为物理删除

## BR-H06: Signal 规则
- 项目创建/更新后发送 `heritage_item_saved` 信号（供 search 模块同步索引）
- 项目删除后发送 `heritage_item_deleted` 信号（供 search 和 media 清理）

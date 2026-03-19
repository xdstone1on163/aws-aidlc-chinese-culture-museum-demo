# 非遗博物馆 - 工作单元依赖关系

## 依赖矩阵

| 单元 ↓ 依赖 → | Unit 1 | Unit 2 | Unit 3 | Unit 4 | Unit 5 | Unit 6 |
|----------------|--------|--------|--------|--------|--------|--------|
| **Unit 1** 核心与认证 | - | - | - | - | - | - |
| **Unit 2** 媒体管理 | ✅ | - | - | - | - | - |
| **Unit 3** 非遗内容管理 | ✅ | ✅ | - | - | - | - |
| **Unit 4** 评价与搜索 | ✅ | ✅ | ✅ | - | - | - |
| **Unit 5** 前端应用 | ✅ | ✅ | ✅ | ✅ | - | - |
| **Unit 6** 社区论坛 | ✅ | - | - | - | ✅ | - |

✅ = 行单元依赖列单元

---

## 开发顺序图

```
Unit 1 (核心与认证)
  │
  ├──→ Unit 2 (媒体管理)
  │      │
  │      ├──→ Unit 3 (非遗内容管理)
  │      │      │
  │      │      ├──→ Unit 4 (评价与搜索)
  │      │      │      │
  │      │      │      └──→ Unit 5 (前端应用)
  │      │      │                │
  │      │      │                └──→ Unit 6 (社区论坛) [P1]
  │      │      │
```

---

## 依赖说明

| 依赖关系 | 说明 |
|----------|------|
| Unit 2 → Unit 1 | media 需要 core 公共模块和 accounts 认证 |
| Unit 3 → Unit 1 | heritage 需要 core 和 accounts 权限校验 |
| Unit 3 → Unit 2 | heritage 通过 MediaService 关联媒体文件 |
| Unit 4 → Unit 1 | reviews 需要 accounts 用户信息 |
| Unit 4 → Unit 2 | reviews 评论图片通过 media 上传 |
| Unit 4 → Unit 3 | reviews 关联 heritage 项目；search 从 heritage 同步索引 |
| Unit 5 → Unit 1~4 | 前端调用所有后端 API |
| Unit 6 → Unit 1 | forum 需要 accounts 用户信息 |
| Unit 6 → Unit 5 | 论坛前端基于已有前端框架开发 |

---

## 关键路径

```
Unit 1 → Unit 2 → Unit 3 → Unit 4 → Unit 5 → Unit 6
```

所有单元串行开发，关键路径即为开发顺序。Unit 6 为 P1 优先级，MVP 阶段可暂不开发。

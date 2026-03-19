# 单元测试执行指南

## 后端单元测试

### 运行全部测试
```bash
cd ich_museum
source venv/bin/activate
pytest
```

### 运行带覆盖率报告
```bash
pytest --cov=apps --cov-report=html --cov-report=term
# HTML 报告生成在 htmlcov/ 目录
```

### 按模块运行
```bash
pytest apps/accounts/tests/          # 认证模块
pytest apps/media/tests/             # 媒体模块
pytest apps/heritage/tests/          # 非遗内容模块
pytest apps/reviews/tests/           # 评价模块
```

### 运行单个测试
```bash
pytest apps/accounts/tests/test_services.py::TestLogin::test_login_success
```

## 测试覆盖范围

### accounts 模块（Unit 1）
| 测试文件 | 测试内容 | 用例数 |
|----------|----------|--------|
| test_models.py | User/Profile/Token 模型创建和约束 | 5 |
| test_services.py | 注册/验证/登录/重置/禁用/角色管理 | 11 |
| test_views.py | API 端点（注册/登录/验证/个人信息/管理） | 10 |

### media 模块（Unit 2）
| 测试文件 | 测试内容 | 用例数 |
|----------|----------|--------|
| test_services.py | 上传/批量上传/封面/删除 | 5 |

### heritage 模块（Unit 3）
| 测试文件 | 测试内容 | 用例数 |
|----------|----------|--------|
| test_services.py | CRUD/状态变更/收藏 | 6 |

### reviews 模块（Unit 4）
| 测试文件 | 测试内容 | 用例数 |
|----------|----------|--------|
| test_services.py | 创建/更新评分/回复/删除/统计 | 7 |

## 预期结果
- 总测试用例：~44 个
- 目标覆盖率：核心业务逻辑 ≥ 80%
- 全部通过，0 失败

## 代码质量检查
```bash
ruff check apps/
ruff format --check apps/
```

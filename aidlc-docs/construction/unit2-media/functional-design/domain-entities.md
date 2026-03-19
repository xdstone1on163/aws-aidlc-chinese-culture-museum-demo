# Unit 2: 媒体管理 - 领域实体

## MediaFile（媒体文件）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK, auto | 主键 |
| file | FileField | NOT NULL | 文件路径（Django FileSystemStorage） |
| original_name | CharField(255) | NOT NULL | 原始文件名 |
| file_type | CharField(20) | NOT NULL | 文件类型：image / video / audio |
| mime_type | CharField(100) | NOT NULL | MIME 类型（image/jpeg 等） |
| file_size | BigIntegerField | NOT NULL | 文件大小（字节） |
| object_type | CharField(50) | NOT NULL | 关联对象类型（heritage_item / review / user_avatar） |
| object_id | UUIDField | NOT NULL | 关联对象 ID |
| uploaded_by | ForeignKey(User) | NOT NULL | 上传者 |
| sort_order | IntegerField | default=0 | 排序顺序 |
| is_cover | BooleanField | default=False | 是否为封面图 |
| created_at | DateTimeField | auto_now_add | 上传时间 |

**索引**: (object_type, object_id) 联合索引，加速按对象查询媒体文件

**说明**: 使用通用外键模式（object_type + object_id），而非 Django GenericForeignKey，保持简单和可查询性。

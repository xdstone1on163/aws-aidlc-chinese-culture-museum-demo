# Unit 2: 媒体管理 - 业务流程

## 1. 文件上传流程

```
客户端提交 multipart/form-data (file, object_type, object_id)
  │
  ├─ 校验认证 → 未登录 → 401
  ├─ 校验权限 → 无权限 → 403
  ├─ 校验 file_type (根据 MIME 和扩展名) → 不支持 → 400
  ├─ 校验 file_size → 超限 → 400 "文件大小超过限制"
  │
  ├─ 生成存储路径: media/{object_type}/{YYYY}/{MM}/{uuid}.{ext}
  ├─ 保存文件到本地磁盘 (Django FileSystemStorage)
  ├─ 创建 MediaFile 记录
  │
  └─ 返回 201 + MediaFile 元数据 (id, url, file_type, file_size)
```

## 2. 批量上传流程

```
客户端提交 multipart/form-data (files[], object_type, object_id)
  │
  ├─ 逐个校验每个文件 (类型、大小)
  ├─ 任一文件校验失败 → 400 (返回失败文件列表)
  │
  ├─ 逐个保存文件并创建 MediaFile 记录
  │
  └─ 返回 201 + 所有 MediaFile 元数据列表
```

## 3. 设置封面图

```
客户端提交 PATCH (media_id, is_cover=true)
  │
  ├─ 校验 media_id 存在且为图片类型
  ├─ 取消同对象下其他封面 (UPDATE is_cover=false WHERE object_type+object_id)
  ├─ 设置当前图片为封面
  │
  └─ 返回 200
```

## 4. 删除媒体文件

```
客户端提交 DELETE (media_id)
  │
  ├─ 校验权限
  ├─ 删除本地文件
  ├─ 删除 MediaFile 记录
  │
  └─ 返回 204
```

## 故事覆盖

| 故事 | 覆盖状态 |
|------|----------|
| US-C03 管理多媒体资源 | ✅ 上传、批量上传、排序、删除、设置封面 |

"""Heritage item models."""
import uuid
from django.conf import settings
from django.db import models


class Category(models.Model):
    """Non-heritage category (10 national categories, fixture-loaded)."""
    name = models.CharField(max_length=50, unique=True, verbose_name='分类名称')
    name_en = models.CharField(max_length=100, blank=True, default='', verbose_name='英文名称')
    code = models.CharField(max_length=20, unique=True, verbose_name='分类编码')
    sort_order = models.IntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'heritage_category'
        ordering = ['sort_order']
        verbose_name = '非遗分类'
        verbose_name_plural = '非遗分类'

    def __str__(self):
        return self.name


class Region(models.Model):
    """Geographic region."""
    name = models.CharField(max_length=50, unique=True, verbose_name='地域名称')
    name_en = models.CharField(max_length=100, blank=True, default='', verbose_name='英文名称')

    class Meta:
        db_table = 'heritage_region'
        ordering = ['name']
        verbose_name = '地域'
        verbose_name_plural = '地域'

    def __str__(self):
        return self.name


class Inheritor(models.Model):
    """Heritage inheritor / practitioner."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='姓名')
    name_en = models.CharField(max_length=200, blank=True, default='')
    title = models.CharField(max_length=100, blank=True, default='', verbose_name='称号')
    bio = models.TextField(blank=True, default='', verbose_name='简介')
    bio_en = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'heritage_inheritor'
        verbose_name = '传承人'
        verbose_name_plural = '传承人'

    def __str__(self):
        return self.name


class ItemStatus(models.TextChoices):
    DRAFT = 'draft', '草稿'
    PUBLISHED = 'published', '已发布'
    ARCHIVED = 'archived', '已下架'


class HeritageItem(models.Model):
    """Core heritage item."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name='项目名称')
    name_en = models.CharField(max_length=400, blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items', verbose_name='分类')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    summary = models.TextField(max_length=500, verbose_name='简介摘要')
    summary_en = models.TextField(max_length=500, blank=True, default='')
    description = models.TextField(verbose_name='详细描述 (Markdown)')
    description_en = models.TextField(blank=True, default='')
    history = models.TextField(blank=True, default='', verbose_name='历史背景')
    history_en = models.TextField(blank=True, default='')
    inheritors = models.ManyToManyField(Inheritor, blank=True, related_name='heritage_items', verbose_name='传承人')
    status = models.CharField(max_length=20, choices=ItemStatus.choices, default=ItemStatus.DRAFT, verbose_name='状态')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'heritage_item'
        ordering = ['-created_at']
        verbose_name = '非遗项目'
        verbose_name_plural = '非遗项目'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """User favorite heritage item."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    heritage_item = models.ForeignKey(HeritageItem, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'heritage_favorite'
        unique_together = ('user', 'heritage_item')
        ordering = ['-created_at']
        verbose_name = '收藏'
        verbose_name_plural = '收藏'

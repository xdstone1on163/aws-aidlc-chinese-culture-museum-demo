"""Heritage test factories."""
import factory
from apps.heritage.models import Category, Region, HeritageItem, ItemStatus
from apps.accounts.tests.factories import UserFactory, ContentManagerFactory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('code',)

    name = factory.Sequence(lambda n: f'分类{n}')
    name_en = factory.Sequence(lambda n: f'Category {n}')
    code = factory.Sequence(lambda n: f'cat_{n}')
    sort_order = factory.Sequence(lambda n: n)


class RegionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Region
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'地区{n}')
    name_en = factory.Sequence(lambda n: f'Region {n}')


class HeritageItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = HeritageItem

    name = factory.Sequence(lambda n: f'非遗项目{n}')
    category = factory.SubFactory(CategoryFactory)
    region = factory.SubFactory(RegionFactory)
    summary = '这是一个非遗项目的简介'
    description = '# 详细描述\n\n这是 Markdown 格式的详细描述。'
    status = ItemStatus.PUBLISHED
    created_by = factory.SubFactory(ContentManagerFactory, profile=None)

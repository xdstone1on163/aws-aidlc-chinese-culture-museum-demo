"""Heritage serializers."""
from rest_framework import serializers
from .models import HeritageItem, Category, Region, Inheritor, Favorite


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_en', 'code']


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'name_en']


class InheritorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inheritor
        fields = ['id', 'name', 'name_en', 'title', 'bio', 'bio_en']


class HeritageItemListSerializer(serializers.ModelSerializer):
    """List view - minimal fields."""
    category_name = serializers.CharField(source='category.name', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True, default='')
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = HeritageItem
        fields = ['id', 'name', 'name_en', 'summary', 'summary_en',
                  'category_name', 'region_name', 'status', 'is_favorited', 'created_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, heritage_item=obj).exists()
        return False


class HeritageItemDetailSerializer(serializers.ModelSerializer):
    """Detail view - all fields."""
    category = CategorySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    inheritors = InheritorSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = HeritageItem
        fields = ['id', 'name', 'name_en', 'category', 'region', 'summary', 'summary_en',
                  'description', 'description_en', 'history', 'history_en',
                  'inheritors', 'status', 'is_favorited', 'created_by', 'created_at', 'updated_at']

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, heritage_item=obj).exists()
        return False


class HeritageItemCreateSerializer(serializers.ModelSerializer):
    inheritor_ids = serializers.ListField(child=serializers.UUIDField(), required=False, write_only=True)

    class Meta:
        model = HeritageItem
        fields = ['name', 'name_en', 'category', 'region', 'summary', 'summary_en',
                  'description', 'description_en', 'history', 'history_en',
                  'status', 'inheritor_ids']

    def create(self, validated_data):
        inheritor_ids = validated_data.pop('inheritor_ids', [])
        from . import services
        item = services.create_item(validated_data, self.context['request'].user)
        if inheritor_ids:
            item.inheritors.set(Inheritor.objects.filter(id__in=inheritor_ids))
        return item

    def update(self, instance, validated_data):
        inheritor_ids = validated_data.pop('inheritor_ids', None)
        from . import services
        item = services.update_item(instance, validated_data)
        if inheritor_ids is not None:
            item.inheritors.set(Inheritor.objects.filter(id__in=inheritor_ids))
        return item


class FavoriteSerializer(serializers.ModelSerializer):
    heritage_item = HeritageItemListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'heritage_item', 'created_at']

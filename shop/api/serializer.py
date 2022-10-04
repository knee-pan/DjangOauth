from datetime import timezone

from rest_framework import serializers

from shop.models import Category, Product


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created", "updated"]


# lookup_field=pk
class ProductUpdateCreateSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["id", "created", "updated"]

    def create(self, validated_data):
        return Product.objects.create(**validated_data).save()
        # Product.objects.create(user=self.context['request'].user,**validated_data)

    # sadece updateApiView ile çalışır, pk ile gidin
    def update(self, instance, validated_data):
        instance.updated = validated_data.get("updated", instance.updated)
        instance.save()
        return instance

    # def validate_updated(self, value):
    #     """spesifik bir durum için validate islemi"""
    #     if isinstance(value, None):
    #         raise serializers.ValidationError("updated None olamaz")
    #     return value

    # def validate(self, attrs):
    #     if attrs["created"] < attrs["updated"]:
    #         raise serializers.ValidationError("Error")
    #     return attr

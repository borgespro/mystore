from django.db.models import Sum
from rest_framework import serializers

from apps.products.models import Category, Product, KitAttribute


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'saleable')


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'description', 'type', 'unit_price')


class KitAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = KitAttribute
        fields = ('id', 'category', 'name', 'required')


class KitSerializer(serializers.ModelSerializer):
    kit_attributes = KitAttributeSerializer(many=True, read_only=True)
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'description', 'kit_attributes')


class KitAttValueSerializer(serializers.ModelSerializer):
    value = ProductSerializer(many=False, read_only=True)
    available_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'value', 'available_quantity')

    def get_available_quantity(self, instance):
        return instance.value.get_available_quantity()




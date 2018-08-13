from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import Product, KitAttribute
from .models import SaleOrder, SaleOrderLine
from apps.core.models import User


class SaleOrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrderLine
        fields = ('product', 'kit', 'quantity', 'price', 'attribute')


class SaleOrderSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    status = serializers.ReadOnlyField()
    total_price = serializers.SerializerMethodField()
    sale_lines = SaleOrderLineSerializer(many=True)

    class Meta:
        model = SaleOrder
        fields = ('id', 'status', 'customer', 'sale_lines', 'total_price')

    def validate(self, data):
        customer = data.get('customer')
        if customer.user_type != User.CUSTOMER:
            raise ValidationError('User is not customer!')
        sale_lines = data['sale_lines']
        kits = {}
        for line in sale_lines:
            kit = line.get('kit')
            attribute = line.get('attribute')

            if kit and not attribute:
                raise ValidationError('The attribute field is required for kits.')
            elif kit and kit not in kits:
                kit_queryset = kit.kit_attributes.all()
                attr_obj = kit_queryset.filter(name=attribute).first()
                if attr_obj and not attr_obj.values.filter(value=line['product']).exists():
                    raise ValidationError('This product is not allowed.')
                kits[kit] = {att.name for att in kit_queryset if attribute != att.name}
            elif kit and kit in kits:
                try:
                    kits[kit].remove(attribute)
                except KeyError:
                    raise ValidationError('Attribute {} in kit {} is not allowed'.format(attribute, kit))

            if line['product'].type != Product.SIMPLE:
                raise ValidationError('Field product in "sale_lines" should be a Simple Product.')
            if line['product'].get_available_quantity() <= 0:
                raise ValidationError('{} is not available'.format(line['product']))
            if kit and kit.type != Product.KIT:
                raise ValidationError('Field kit in "sale_lines" should be a Kit Product.')
            elif not kit and not line['product'].category.saleable:
                raise ValidationError('Field product could not filled with not saleable product.')

        for kit, attrs in kits.items():
            not_required_attrs = {att.name for att in kit.kit_attributes.all() if not att.required}
            attrs_diff = attrs.difference(not_required_attrs)
            if attrs and attrs_diff:
                raise ValidationError('Attribute[s] {} in kit {} is required.'.format(attrs_diff, kit))

        return super(SaleOrderSerializer, self).validate(data)

    def create(self, validated_data):
        sale_lines_data = validated_data.pop('sale_lines')
        sale_order = SaleOrder.objects.create(**validated_data)
        for sale_line_data in sale_lines_data:
            SaleOrderLine.objects.create(sale_order=sale_order, **sale_line_data)
        return sale_order

    def get_total_price(self, instance):
        return instance.get_total_price()

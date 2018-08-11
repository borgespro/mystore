import django_filters

from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = ['category', ]

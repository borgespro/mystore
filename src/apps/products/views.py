from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import ProductFilter
from .models import Category, Product, KitAttValue, KitAttribute
from .serializers import CategorySerializer, ProductSerializer, KitSerializer, KitAttValueSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SaleableCategoryList(CategoryList):
    queryset = Category.objects.filter(saleable=True)


class BaseProductList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter


class ProductList(BaseProductList):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class KitList(BaseProductList):
    queryset = Product.objects.filter(type=Product.KIT)
    serializer_class = KitSerializer


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        product = self.get_object()
        if product and product.type == Product.KIT:
            return KitSerializer
        else:
            return ProductSerializer


class KitDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(type=Product.KIT)
    serializer_class = KitSerializer


class AttributeValueList(generics.ListAPIView):
    serializer_class = KitAttValueSerializer

    def get_queryset(self):
        attribute_id = self.kwargs.get('attribute_id')
        if attribute_id and KitAttribute.objects.filter(pk=attribute_id).exists():
            return KitAttValue.objects.filter(attribute=attribute_id).prefetch_related('value').order_by('id')
        else:
            raise Http404('Kit Attribute not found!')

from django.urls import path
from .views import CategoryList, SaleableCategoryList, ProductList, KitList, ProductDetail, KitDetail, \
    AttributeValueList

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('kits/', KitList.as_view(), name='kit_list'),
    path('kits/attributes/<int:attribute_id>/values/', AttributeValueList.as_view(), name='attribute_value_list'),
    path('kits/<int:pk>/', KitDetail.as_view(), name='kit_detail'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/saleable/', SaleableCategoryList.as_view(), name='saleable_category_list'),
]



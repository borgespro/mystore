from django.urls import path
from .views import SaleOrderView


urlpatterns = [
    path('', SaleOrderView.as_view(), name='sale_order'),
]

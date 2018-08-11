from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from .views import UserCreate

urlpatterns = [
    path('auth/', obtain_jwt_token, name='login'),
    path('customer/register/', UserCreate.as_view(), name='register'),
]

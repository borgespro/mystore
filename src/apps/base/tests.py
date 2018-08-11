from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.stocks.models import Warehouse

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name='My Warehouse', address='St. Warehouse, 100, London')

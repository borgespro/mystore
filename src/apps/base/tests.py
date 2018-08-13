from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from django.urls import reverse

from apps.stocks.models import Warehouse

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name='My Warehouse', address='St. Warehouse, 100, London')
        self.john_lennon = User.objects\
            .create_user('john', 'lennon@thebeatles.com', 'johnpassword', user_type='CUSTOMER')
        self.john_lennon_token = self._get_jwt_token('john', 'johnpassword')
        self.admin = User.objects\
            .create_user('admin', 'admin@admin.com', 'admin', user_type='ADMIN')
        self.admin_token = self._get_jwt_token('admin', 'admin')

    def _get_jwt_token(self, username, password):
        url_login = reverse('login')
        return self.client.post(url_login, {'username': username, 'password': password}, format='json').data['token']

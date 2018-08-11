from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from django.urls import reverse

User = get_user_model()


class BaseAPITest(APITestCase):
    def setUp(self):
        pass

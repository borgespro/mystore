from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_login_with_valid_credentials(self):
        url_login = reverse('login')
        payload = {'username': 'john', 'password': 'johnpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsNotNone(response.data.get('token'))

    def test_login_with_invalid_credentials(self):
        url_login = reverse('login')
        payload = {'username': 'lennon', 'password': 'wrongpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIsNotNone(response.data.get('non_field_errors'))

    def test_login_with_invalid_payload(self):
        url_login = reverse('login')
        payload = {'email': 'john', 'password': 'johnpassword'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(response.data, dict)
        self.assertIsNone(response.data.get('non_field_errors'))
        self.assertIsNotNone(response.data.get('username'))

    def test_create_customer_with_complete_information(self):
        url_register = reverse('register')
        payload = {
            'first_name': 'Paul',
            'last_name': 'McCartney',
            'email': 'paul.mccartney@borges.pro',
            'phone': '+44 55 88 77 666 44',
            'password': 'paulpassword123',
            'address': '1 Soho Square London W1D 3BQ UK'
        }
        response = self.client.post(url_register, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_register, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url_login = reverse('login')
        customer = User.objects.get(email=payload['email'])
        self.assertEqual(customer.first_name, payload['first_name'])
        self.assertEqual(customer.last_name, payload['last_name'])
        self.assertEqual(customer.email, payload['email'])
        self.assertEqual(customer.username, payload['email'])
        self.assertEqual(customer.address, payload['address'])
        self.assertEqual(customer.user_type, User.CUSTOMER)
        payload = {'username': 'paul.mccartney@borges.pro', 'password': 'paulpassword123'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIsNotNone(response.data.get('token'))

    def test_create_customer_with_incomplete_information(self):
        url_register = reverse('register')
        payload = {
            'first_name': 'Paul',
            'last_name': 'McCartney',
            'email': 'paul.mccartney@borges.pro',
            'password': 'paulpassword123',
        }
        response = self.client.post(url_register, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        url_login = reverse('login')
        self.assertRaises(User.DoesNotExist, lambda: User.objects.get(email=payload['email']))
        payload = {'username': 'paul.mccartney@borges.pro', 'password': 'paulpassword123'}
        response = self.client.post(url_login, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

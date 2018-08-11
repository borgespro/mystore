from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'ADMIN'
    CUSTOMER = 'CUSTOMER'

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
    )

    user_type = models.CharField('Tipo de usuário', max_length=12, choices=USER_TYPES, default=CUSTOMER)
    phone = models.CharField('Telefone', max_length=20)
    address = models.TextField('Endereço', blank=True)

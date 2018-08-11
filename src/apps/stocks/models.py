from django.db import models

from apps.base.models import BaseModel


class Warehouse(BaseModel):
    address = models.TextField('Endereço', db_index=True)

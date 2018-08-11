from django.db import models

from apps.base.models import BaseModel
from apps.products.models import Product


class Warehouse(BaseModel):
    name = models.CharField('Nome', max_length=50, db_index=True)
    address = models.TextField('Endereço', db_index=True)

    class Meta:
        verbose_name = 'Armazém'
        verbose_name_plural = 'Armazéns'

    def __str__(self):
        return '{} - {}'.format(self.name, self.address)


class StockMovement(BaseModel):
    warehouse = models.ForeignKey('Warehouse', verbose_name='Armazén', on_delete=models.CASCADE)
    date = models.DateTimeField('Data', db_index=True)

    class Meta:
        verbose_name = 'Movimentação de estoque'
        verbose_name_plural = 'Movimentações de estoque'

    def __str__(self):
        return '{} - {}'.format(self.date, self.warehouse)


class StockMovementLine(BaseModel):
    stock = models.ForeignKey('StockMovement', verbose_name='Movimentação de estoque', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        db_index=True,
        limit_choices_to={'type': Product.SIMPLE}
    )
    quantity = models.DecimalField('Quantidade', default=0.0, decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Movimentação de estoque'
        verbose_name_plural = 'Movimentações de estoque'
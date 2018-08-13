from django.conf import settings
from django.db import models
from django.utils.datetime_safe import datetime

from apps.base.models import BaseModel
from apps.products.models import Product
from apps.core.models import User
from apps.stocks.models import StockMovement, StockMovementLine


class SaleOrder(BaseModel):
    ORDER_PLACED = 'ORDER_PLACED'
    SEPARATION_IN_STOCK = 'SEPARATION_IN_STOCK'
    MOUNTING = 'MOUNTING'
    REALIZATION_OF_TESTS = 'REALIZATION_OF_TESTS'
    DONE = 'DONE'

    STATUS = (
        (ORDER_PLACED, 'Pedido Realizado'),
        (SEPARATION_IN_STOCK, 'Em Separação no Estoque'),
        (MOUNTING, 'Em Montagem'),
        (REALIZATION_OF_TESTS, 'Realização de Testes'),
        (DONE, 'Concluído'),
    )

    status = models.CharField('Status', choices=STATUS, max_length=40, default=ORDER_PLACED)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'

    def get_total_price(self):
        return sum([line.price for line in self.sale_lines.all()])


class SaleOrderLine(BaseModel):
    sale_order = models.ForeignKey('SaleOrder', on_delete=models.CASCADE, related_name='sale_lines')
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.DO_NOTHING,
        related_name='product_order_lines',
        limit_choices_to={'type': Product.SIMPLE}
    )
    kit = models.ForeignKey(
        'products.Product',
        on_delete=models.DO_NOTHING,
        null=True,
        related_name='kit_order_lines',
        limit_choices_to={'type': Product.KIT}
    )
    attribute = models.CharField('Atributo', max_length=40, default='DEFAULT')
    quantity = models.IntegerField('Quantidade', default=1)

    def _order_line_price(self):
        return self.quantity * self.product.unit_price
    price = property(_order_line_price)

    def save(self, **kwargs):
        last_stock_line = self.product.stock_lines.filter(product=self.product).last()
        if last_stock_line:
            warehouse = last_stock_line.stock.warehouse
            self.stock_movement = StockMovement.objects.create(warehouse=warehouse, date=datetime.now())
            StockMovementLine.objects.create(stock=self.stock_movement, product=self.product, quantity=-self.quantity)
        return super(SaleOrderLine, self).save(**kwargs)

    class Meta:
        verbose_name = 'Linha do Pedido'
        verbose_name_plural = 'Linhas dos Pedidos'
        ordering = ['sale_order', 'kit', 'product']


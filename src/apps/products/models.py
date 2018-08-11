from django.core.exceptions import ValidationError
from django.db import models

from apps.base.models import BaseModel


class Category(BaseModel):
    name = models.CharField('Nome', max_length=40, db_index=True)
    saleable = models.BooleanField('Vendável', default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(BaseModel):
    KIT = 'KIT'
    SIMPLE = 'SIMPLE'

    PRODUCT_TYPES = (
        (KIT, 'Kit'),
        (SIMPLE, 'Simples')
    )

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField('Nome', max_length=40, db_index=True)
    description = models.TextField('Descrição', blank=True)
    type = models.CharField('Tipo', max_length=10, choices=PRODUCT_TYPES)
    unit_price = models.DecimalField('Preço unitário', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('name',)

    def __str__(self):
        return '{} (Cat: {})'.format(self.name, self.category)


def validate_kit(value):
    if value.type != Product.KIT:
        raise ValidationError(
            _('%(value) is not a Kit.'),
            params={'value': value},
        )


class KitAttribute(BaseModel):
    kit = models.ForeignKey(
        'Product',
        verbose_name='Kit',
        on_delete=models.CASCADE,
        related_name='kit_attributes',
        limit_choices_to={'type': Product.KIT},
        validators=[validate_kit],
    )
    category = models.ForeignKey('Category', verbose_name='Categoria', on_delete=models.CASCADE)
    required = models.BooleanField('Requerido', default=True)
    name = models.CharField('Nome', max_length=40, db_index=True)

    class Meta:
        verbose_name = 'Atributo'
        verbose_name_plural = 'Atributos'
        ordering = ('name',)

    def __str__(self):
        return '{} - {}'.format(self.name, self.kit)


class KitAttValue(BaseModel):
    attribute = models.ForeignKey('KitAttribute', verbose_name='Atributo', on_delete=models.CASCADE)
    value = models.ForeignKey('Product', verbose_name='Valor', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Valor de Atributo'
        verbose_name_plural = 'Valores de Atributos'

    def __str__(self):
        return '{} - {}'.format(self.attribute, self.value)


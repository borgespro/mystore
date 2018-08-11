from django.contrib import admin

from apps.base.admin import BaseModelAdmin
from apps.products.models import Product, Category, KitAttribute, KitAttValue


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    pass


@admin.register(KitAttribute)
class KitAttributeAdmin(BaseModelAdmin):
    pass


@admin.register(KitAttValue)
class KitAttValueAdmin(BaseModelAdmin):
    pass

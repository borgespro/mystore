from django.contrib import admin

from apps.base.admin import BaseModelAdmin
from apps.products.models import Product, Category, KitAttribute, KitAttValue


@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    pass


class KitAttValueInline(admin.TabularInline):
    extra = 1
    model = KitAttValue


@admin.register(KitAttribute)
class KitAttributeAdmin(BaseModelAdmin):
    inlines = [
        KitAttValueInline,
    ]


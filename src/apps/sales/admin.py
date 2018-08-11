from django.contrib import admin

from apps.base.admin import BaseModelAdmin
from .models import SaleOrder, SaleOrderLine


class SaleOrderLineInline(admin.TabularInline):
    extra = 1
    model = SaleOrderLine


@admin.register(SaleOrder)
class SaleOrderAdmin(BaseModelAdmin):

    inlines = [
        SaleOrderLineInline,
    ]



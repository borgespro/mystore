from django.contrib import admin

from apps.base.admin import BaseModelAdmin
from .models import Warehouse, StockMovement, StockMovementLine


@admin.register(Warehouse)
class WarehouseAdmin(BaseModelAdmin):
    pass


class StockMovementLineInline(admin.TabularInline):
    extra = 1
    model = StockMovementLine


@admin.register(StockMovement)
class StockMovementAdmin(BaseModelAdmin):
    inlines = [
        StockMovementLineInline
    ]

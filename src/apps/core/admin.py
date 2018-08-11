from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models import User


@admin.register(User)
class CoreUserAdmin(UserAdmin):
    pass

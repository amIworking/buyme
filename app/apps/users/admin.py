from django.contrib import admin

# Register your models here.
from ..users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'company', 'position', 'user_type']

from django.contrib import admin
from apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'full_name',
        'email'
    )

    search_fields = (
        'id',
        'full_name',
        'email',
        'username'
    )
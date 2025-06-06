from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    ordering = ['email']
    list_per_page = 20
    list_display_links = ['email']
    search_fields = ['email', 'first_name', 'last_name']

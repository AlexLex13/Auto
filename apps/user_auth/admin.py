from django.contrib import admin

from apps.user_auth.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')
    list_display_links = ('id', )
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['is_active', 'is_staff', 'is_email_verified']
    list_per_page = 10

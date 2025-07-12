from django.contrib import admin

from apps.suppliers.models import Supplier, SupplierCars

admin.site.register(SupplierCars)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'balance')
    list_display_links = ('id', 'name')
    ordering = ['name', '-created_at']
    search_fields = ['name', 'email']
    list_editable = ('balance',)
    list_filter = ['is_active']
    list_per_page = 10

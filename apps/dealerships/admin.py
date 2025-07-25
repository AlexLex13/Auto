from django.utils import timezone
from django.contrib import admin

from apps.dealerships.models import (
    Dealership,
    DealershipCars,
    DealershipPreference,
    Purchase,
    Discount
)


admin.site.register(DealershipCars)
admin.site.register(DealershipPreference)


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'balance')
    list_display_links = ('id', )
    ordering = ['name', '-created_at']
    search_fields = ['name', 'email']
    list_editable = ('balance', )
    list_filter = ['is_active']
    list_per_page = 10


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'dealership', 'car', 'price')
    list_display_links = ('id', )
    ordering = ['-date']
    search_fields = ['dealership__name', 'car__brand', 'car__model']
    list_filter = ['is_active', ]
    list_per_page = 10


class ExpiredDiscountFilter(admin.SimpleListFilter):
    title = 'validity'
    parameter_name = 'is_expired'

    def lookups(self, request, model_admin):
        return [
            ('1', 'expired'),
            ('0', 'unexpired'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(end_from__gte=timezone.now())
        elif self.value() == '1':
            return queryset.filter(end_from__lt=timezone.now())
        else:
            return queryset


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'supplier',
        'dealership',
        'discount_percent',
        'end_from'
    )
    list_display_links = ('id', )
    ordering = ['name', '-created_at', ]
    search_fields = ['name', 'supplier__name', 'dealership__name']
    list_editable = ('name', 'discount_percent')
    list_filter = [ExpiredDiscountFilter, 'is_active']
    list_per_page = 10

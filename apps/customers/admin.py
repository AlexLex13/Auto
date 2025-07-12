import datetime

from django.contrib import admin, messages

from apps.customers.models import Customer, Offer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
    list_display_links = ('id',)
    ordering = ['-created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    list_editable = ('balance',)
    list_filter = ['is_active']
    list_per_page = 10


class ValidOfferFilter(admin.SimpleListFilter):
    title = 'validity'
    parameter_name = 'is_valid'

    def lookups(self, request, model_admin):
        return [
            ('1', 'valid'),
            ('0', 'invalid'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(valid_until__gte=datetime.date.today())
        elif self.value() == '0':
            return queryset.filter(valid_until__lt=datetime.date.today())
        else:
            return queryset


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'max_price', 'valid_until', 'status')
    list_display_links = ('id',)
    ordering = ['-created_at']
    search_fields = ['customer__user__first_name', 'customer__user__last_name']
    list_editable = ('max_price', 'valid_until', 'status')
    list_filter = [ValidOfferFilter, 'is_active', 'car_brand', 'car_model']
    actions = ['set_cancelled', 'set_completed']
    list_per_page = 10

    @admin.action(description="Cancel selected offers")
    def set_cancelled(self, request, queryset):
        count = queryset.update(status=Offer.Status.CANCELLED)
        self.message_user(
            request,
            f"{count} records have been changed.",
            messages.WARNING
        )

    @admin.action(description="Complete selected offers")
    def set_completed(self, request, queryset):
        count = queryset.update(status=Offer.Status.CANCELLED)
        self.message_user(
            request,
            f"{count} records have been changed."
        )

from django.contrib import admin

from apps.cars.models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'brand', 'brief_info')
    list_display_links = ('id',)
    ordering = ['-created_at']
    search_fields = ['colour', 'mileage', 'release_year']
    list_filter = ['model', 'brand', 'is_active']
    list_per_page = 10

    @admin.display(description="description", ordering='release_year')
    def brief_info(self, car):
        return (
            f"The {car.release_year} car is {car.colour} with a mileage "
            f"of {car.mileage} kilometers"
        )

from django.db import models
from djmoney.models.fields import MoneyField

from apps.cars.models import Car
from apps.core.models import TimestampedModel


class Supplier(TimestampedModel):
    """Stores basic information about the supplier."""

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=55)
    established_year = models.PositiveIntegerField()
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    cars = models.ManyToManyField(
        Car,
        related_name='supplier_cars',
        through='SupplierCars'
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(established_year__gte=1850),
                name="established_year_gte_1850"
            ),
        ]

    def __str__(self):
        return self.name


class SupplierCars(TimestampedModel):
    """Auxiliary table linking cars and supplier."""

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )

from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

from apps.cars.models import Car
from apps.core.models import TimestampedModel
from apps.customers.models import Customer
from apps.suppliers.models import Supplier


class Dealership(TimestampedModel):
    """Stores basic information about the dealership."""

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=55)
    location = CountryField()
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    cars = models.ManyToManyField(
        Car,
        related_name='dealership_cars',
        through='DealershipCars'
    )

    def __str__(self):
        return self.name


class DealershipPreference(TimestampedModel):
    """Stores car dealership preferences based on cars characteristics."""

    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    characteristics = models.JSONField()


class DealershipCars(TimestampedModel):
    """Auxiliary table linking cars and car dealerships."""

    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id}_{self.dealership}_{self.car}"


class Discount(TimestampedModel):
    """Stores information about promotions provided
    to car dealerships from suppliers
    """

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_from = models.DateTimeField(auto_now_add=True)
    end_from = models.DateTimeField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)



class Purchase(TimestampedModel):
    """Stores the purchase history."""

    dealership = models.ForeignKey(Dealership, on_delete=models.RESTRICT)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    car = models.ForeignKey(Car, on_delete=models.RESTRICT)
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    discount = models.OneToOneField(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

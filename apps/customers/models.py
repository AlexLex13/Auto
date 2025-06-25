from django.db import models
from djmoney.models.fields import MoneyField

from apps.cars.models import Car, CarModelTypes, CarBrands
from apps.core.models import TimestampedModel


class Customer(TimestampedModel):
    """Stores basic information about the customer."""

    first_name = models.CharField(max_length=55)
    second_name = models.CharField(max_length=55)
    email = models.EmailField(max_length=55)
    age = models.PositiveIntegerField()
    id_card = models.ImageField()
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(age__lte=150), name="age_gte_150"),
        ]


class Offer(TimestampedModel):
    """Stores information about the customer's order"""

    class OfferStatus(models.TextChoices):
        PROCESSED = "PRC", "Processed"
        CANCELLED = "CAN", "Cancelled"
        COMPLETED = "CMP", "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    max_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField()
    valid_until = models.DateField(null=True, blank=True)
    car_model = models.CharField(
        max_length=3,
        choices=CarModelTypes,
        default=CarModelTypes.SEDAN,
    )
    car_brand = models.CharField(
        max_length=3,
        choices=CarBrands,
        default=CarBrands.BMW,
    )
    status = models.CharField(
        max_length=3,
        choices=OfferStatus,
        default=OfferStatus.PROCESSED,
    )

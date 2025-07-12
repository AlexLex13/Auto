from django.db import models
from djmoney.models.fields import MoneyField

from apps.cars.models import Car, CarModelTypes, CarBrands
from apps.core.models import TimestampedModel
from apps.user_auth.models import User


class Customer(TimestampedModel):
    """Stores basic information about the customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    id_card = models.ImageField(null=True, blank=True)
    balance = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD',
        default=0
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(age__lte=150),
                name="age_gte_150"
            ),
        ]

    def __str__(self):
        return self.user.username


class Offer(TimestampedModel):
    """Stores information about the customer's order"""

    class Status(models.TextChoices):
        PROCESSED = "PRC", "Processed"
        CANCELLED = "CAN", "Cancelled"
        COMPLETED = "CMP", "Completed"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    max_price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
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
        choices=Status,
        default=Status.PROCESSED,
    )

    def __str__(self):
        return f"{self.id}_{self.customer}_offer"

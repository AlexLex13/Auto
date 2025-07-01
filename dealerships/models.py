from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField


class TimestampedModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CarModel(TimestampedModel):
    name = models.CharField(max_length=255)
    specs = models.JSONField()


class Dealership(TimestampedModel):
    name = models.CharField(max_length=255)
    location = CountryField()
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')


class DealershipPreference(TimestampedModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    preference_detail = models.JSONField(null=True, blank=True)


class Car(TimestampedModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')


class Customer(TimestampedModel):
    name = models.CharField(max_length=255)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    profile = models.JSONField()


class Offer(TimestampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    max_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    status = models.CharField(max_length=50, default='pending')


class Sale(TimestampedModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    sale_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    sale_date = models.DateTimeField(auto_now_add=True)


class Supplier(TimestampedModel):
    name = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField()
    contact_info = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(established_year__gte=1850), name="established_year_gte_1850"),
        ]


class SupplierCarOffer(TimestampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    quantity = models.PositiveIntegerField()
    valid_until = models.DateField(null=True, blank=True)


class PurchaseFromSupplier(TimestampedModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    purchase_date = models.DateTimeField(auto_now_add=True)


class Promotion(TimestampedModel):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    car_models = models.ManyToManyField(CarModel)

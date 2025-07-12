from django.db import models

from apps.core.models import TimestampedModel


class CarModelTypes(models.TextChoices):
    SEDAN = "SED", "Sedan"
    HATCHBACK = "HAT", "Hatchback"
    COUPE = "COP", "Couple"
    CONVERTIBLE = "CON", "Convertible"
    LIMOUSINE = "LIM", "Limousine"
    VAN = "VAN", "Van"
    MINIVAN = "MVN", "Minivan"
    TRUCK = "TRU", "Truck"
    STATION_WAGON = "SWG", "Station wagon"
    PICKUP = "PIC", "Pickup"
    OFF_ROAD = "OFR", "Off-road car"
    CROSSOVER = "CRS", "Crossover"
    SPORTS = "SPR", "Sports car"


class CarBrands(models.TextChoices):
    BMW = "BMW", "BMW"
    TOYOTA = "TOY", "Toyota"
    PEUGEOT = "PGT", "Peugeot"
    MITSUBISHI = "MTS", "Mitsubishi"
    LEXUS = "LXS", "Lexus"
    FORD = "FRD", "Ford"
    SKODA = "SKD", "Skoda"
    LADA = "LAD", "LADA"
    MERCEDES = "MER", "Mercedes"
    HYUNDAI = "HYU", "Hyundai"
    MAZDA = "MZD", "Mazda"
    AUDI = "AUD", "Audi"
    CITROEN = "CTN", "Citroen"
    RENAULT = "RNL", "Renault"
    VOLKSWAGEN = "VKS", "Volkswagen"


class Car(TimestampedModel):
    """Stores the basic characteristics of the car"""

    model = models.CharField(
        max_length=3,
        choices=CarModelTypes,
        default=CarModelTypes.SEDAN,
    )
    brand = models.CharField(
        max_length=3,
        choices=CarBrands,
        default=CarBrands.BMW,
    )
    release_year = models.PositiveIntegerField()
    colour = models.CharField(max_length=55)
    mileage = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(release_year__gte=1850),
                name="release_year_gte_1850"
            ),
        ]

    def __str__(self):
        return f"{self.id}_{self.model}_{self.brand}"

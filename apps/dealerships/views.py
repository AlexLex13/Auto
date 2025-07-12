from django.db.models import Prefetch
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.cars.models import Car
from apps.cars.serializers import CarSerializer
from apps.core.permissions import IsAdminOrReadOnly, IsOwner
from apps.dealerships.models import (
    Dealership,
    Purchase,
    Discount,
    DealershipCars,
    DealershipPreference
)
from apps.dealerships.serializers import (
    DealershipSerializer,
    PurchaseSerializer,
    DiscountSerializer,
    DealershipCarsSerializer,
    DealershipPreferenceSerializer
)
from apps.suppliers.models import SupplierCars


class DealershipViewSet(viewsets.ModelViewSet):

    serializer_class = DealershipSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        return Dealership.objects.prefetch_related(
            Prefetch('cars', queryset=Car.objects.all())
        )

class DealershipCarsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    serializer_class = DealershipCarsSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return DealershipCars.objects.select_related('supplier')


class DealershipPreferenceViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = DealershipPreference.objects.all()
    serializer_class = DealershipPreferenceSerializer
    permission_classes = (IsAdminUser,)

    @action(detail=True, methods=['get'], url_path='suitable')
    def get_suitable_cars(self, request, pk=None, *args, **kwargs):
        preference = DealershipPreference.objects.get(pk=pk)

        supplier_cars_qs = (
            SupplierCars.objects
            .select_related("car", "supplier")
            .filter(
                car__model=preference.characteristics['car_model'],
                car__brand=preference.characteristics['car_brand'],
                quantity__gte=preference.characteristics['quantity'],
                price__lte=preference.characteristics['price']
            )
        )
        cars = [dc.car for dc in supplier_cars_qs]

        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)


class PurchaseViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class DiscountViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAdminUser,)

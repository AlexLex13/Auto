from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.cars.models import Car
from apps.suppliers.models import Supplier
from apps.suppliers.serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):

    serializer_class = SupplierSerializer
    permission_classes = (IsAdminUser, )

    def get_queryset(self):
        return Supplier.objects.prefetch_related(
            Prefetch('cars', queryset=Car.objects.all())
        )

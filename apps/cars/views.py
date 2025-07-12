from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import filters

from apps.cars.models import Car
from apps.cars.serializers import CarSerializer
from apps.core.permissions import IsAdminOrReadOnly


class CarViewSet(viewsets.ModelViewSet):

    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [ filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('model', 'brand')
    search_fields = ['id']
    ordering_fields = ['release_year', 'mileage']

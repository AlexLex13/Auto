from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from apps.cars.serializers import CarSerializer
from apps.core.permissions import IsEmailVerified, IsCustomerOwner, IsOwner
from apps.customers.models import Customer, Offer
from apps.customers.serializers import CustomerSerializer, OfferSerializer
from apps.dealerships.models import DealershipCars


class CustomerViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsCustomerOwner]

    def get_queryset(self):
        return (
            Customer.objects
            .select_related('user')
            .filter(user=self.request.user)
        )


class OfferViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsEmailVerified, IsOwner]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

    @action(detail=True, methods=['get'], url_path='suitable')
    def get_suitable_cars(self, request, pk=None, *args, **kwargs):
        offer = Offer.objects.get(pk=pk)

        dealership_cars_qs = (
            DealershipCars.objects
            .select_related("car", "dealership")
            .filter(
                car__model=offer.car_model,
                car__brand=offer.car_brand,
                quantity__gte=offer.quantity,
                price__lte=offer.max_price
            )
        )
        cars = [dc.car for dc in dealership_cars_qs]

        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

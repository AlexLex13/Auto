from rest_framework import serializers

from apps.cars.models import Car
from apps.suppliers.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    cars = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='car-detail'
    )

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'established_year', 'balance', 'cars']

from rest_framework import serializers

from apps.dealerships.models import (
    Dealership,
    DealershipPreference,
    Purchase,
    Discount,
    DealershipCars
)


class DealershipCarsSerializer(serializers.ModelSerializer):
    supplier = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='supplier-detail'
    )

    class Meta:
        model = DealershipCars
        fields = [
            'id',
            'dealership',
            'car',
            'quantity',
            'price',
            'supplier'
        ]


class DealershipSerializer(serializers.ModelSerializer):
    cars = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='car-detail'
    )

    class Meta:
        model = Dealership
        fields = ['id', 'name', 'email', 'location', 'balance', 'cars']


class DealershipPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipPreference
        fields = ['id', 'dealership', 'characteristics']


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'id',
            'dealership',
            'customer',
            'supplier',
            'car',
            'price',
            'date',
            'quantity'
        ]


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'id',
            'supplier',
            'dealership',
            'name',
            'description',
            'start_from',
            'end_from',
            'discount_percent'
        ]

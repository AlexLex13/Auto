from rest_framework import serializers

from apps.cars.models import Car


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ['model', 'brand', 'release_year', 'colour', 'mileage']

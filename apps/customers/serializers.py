import datetime

from rest_framework import serializers

from apps.customers.models import Customer, Offer
from apps.user_auth.serializers import UserInfoSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()

    class Meta:
        model = Customer
        fields = ['id', 'user', 'age', 'id_card', 'balance']
        read_only_fields = ['balance']

    def update(self, instance, validated_data):
        user = instance.user
        instance.age = validated_data['age']
        instance.id_card = validated_data['id_card']
        instance.save()
        user.first_name = validated_data['user']['first_name']
        user.last_name = validated_data['user']['last_name']
        user.save()
        return instance


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'id',
            'max_price',
            'quantity',
            'valid_until',
            'car_model',
            'car_brand',
            'customer'
        ]
        read_only_fields = ['customer']

    def validate_max_price(self, value):
        """
        Check that max_price is less than balance.
        """
        customer = self.context['request'].user.customer

        if customer.balance < value:
            raise serializers.ValidationError(
                "There are not enough funds on the "
                "balance sheet for such a price"
            )
        return value

    def validate_valid_until(self, value):
        """
        Check that valid_until is greater than current date
        """
        if value <= datetime.date.today():
            raise serializers.ValidationError(
                "Expiration date should be more than today"
            )
        return value
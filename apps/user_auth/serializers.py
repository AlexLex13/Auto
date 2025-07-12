from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import send_mail

from apps.customers.models import Customer
from apps.user_auth.utils import email_verification_token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.send_verification_email(user)
        Customer.objects.create(user=user)
        return user

    def send_verification_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        url = self.context['request'].build_absolute_uri(
            reverse(
                'auth-verify-email',
                kwargs={'uidb64': uid, 'token': token}
            )
        )
        send_mail(
            subject='Verify your email',
            message=f'Click to verify: {url}',
            from_email=None,
            recipient_list=[user.email],
        )


class UserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField()


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    new_password_again = serializers.CharField()

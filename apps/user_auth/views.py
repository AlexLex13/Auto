from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_str, force_bytes
from django.urls import reverse
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from apps.user_auth.serializers import (
    RegisterSerializer, ChangeEmailSerializer, ChangeUsernameSerializer,
    ChangePasswordSerializer, ResetPasswordSerializer, SetNewPasswordSerializer
)
from apps.user_auth.utils import email_verification_token

User = get_user_model()


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=['get'],
        url_path='verify-email/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)',
        name='verify-email'
    )
    def verify_email(self, request, uidb64=None, token=None):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid UID'}, status=400)

        if email_verification_token.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response({'success': 'Email verified'})
        return Response({'error': 'Invalid token'}, status=400)

    @action(detail=False, methods=['post'], url_path='change-email')
    def change_email(self, request):
        serializer = ChangeEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.email = serializer.validated_data['new_email']
        user.is_email_verified = False
        user.save()

        RegisterSerializer(
            context={'request': request}
        ).send_verification_email(user)

        return Response(
            {'status': 'Email change requested. Confirm new email.'})

    @action(detail=False, methods=['post'], url_path='change-username')
    def change_username(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.username = serializer.validated_data['new_username']
        user.save()
        return Response({'status': 'Username changed successfully.'})

    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=400
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'Password changed successfully'})

    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse(
                    'auth-reset-password-confirm',
                    kwargs={'uidb64': uid, 'token': token}
                )
            )
            send_mail(
                subject="Reset your password",
                message=f"Click here to reset your password: {reset_url}",
                from_email=None,
                recipient_list=[email],
            )

        return Response(
            {'status': 'If user exists, password reset email sent.'}
        )

    @action(
        detail=False,
        methods=['post'],
        url_path='reset-password-confirm/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)',
        name='reset-password-confirm'
    )
    def reset_password_confirm(self, request, uidb64=None, token=None):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid link'}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response(
                {'error': 'Invalid or expired token'},
                status=400
            )

        if (serializer.validated_data['new_password'] !=
                serializer.validated_data['new_password_again']):
            return Response(
                {'error': 'Passwords are not the same'},
                status=400
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'Password has been reset.'})

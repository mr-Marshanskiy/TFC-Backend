from crum import get_current_user
from django.contrib.auth import get_user_model
from django_rest_passwordreset.views import HTTP_USER_AGENT_HEADER, \
    HTTP_IP_ADDRESS_HEADER
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.mixins.permissions import PublicMixin
from users.models.confirm import EmailConfirmToken, ResetPasswordToken
from users.serializers.auth import PasswordSerializer

token_param = openapi.Parameter('token', openapi.IN_PATH, description="Token", type=openapi.TYPE_STRING)

User = get_user_model()


class EmailConfirmView(PublicMixin, APIView):
    @swagger_auto_schema(manual_parameters=[token_param], operation_summary="Подтвердить email", tags=['Пользователь'])
    def post(self, request, token):
        token_obj = get_object_or_404(EmailConfirmToken, key=token)
        token_obj.user.email_is_verified = True
        token_obj.user.save()
        token_obj.user.email_confirm_tokens.all().delete()
        return Response({'detail': 'Email подтвержден'})


class EmailConfirmSendView(IsAuthenticated, APIView):
    @swagger_auto_schema(operation_summary="Запросить ссылку для подтверждения email", tags=['Пользователь'])
    def post(self, request):
        if request.user.email_is_verified is False:
            try:
                token = EmailConfirmToken(user=get_current_user())
                token.save()
                return Response({'detail': 'Ссылка отправлена'})
            except Exception as e:
                return Response({'detail': 'Что-то пошло не так'}, 500)
        return Response({'detail': 'Ваш email уже подтвержден'}, 400)


contact_param = openapi.Parameter('contact', openapi.IN_FORM, description="Телефон, email", type=openapi.TYPE_STRING)


class PasswordResetTokenView(PublicMixin, APIView):

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
        }), operation_summary="Запросить ссылку для сброса пароля", tags=['Регистрация и аутентификация']
    )
    def post(self, request):
        email = request.data.get('email', None)
        user = get_object_or_404(User, email__iexact=email,
                                 email_is_verified=True)

        if user.pass_rst_token.all().count() > 0:
            token = user.pass_rst_token.first()
        else:
            token = ResetPasswordToken.objects.create(
                user=user,
                user_agent=request.META.get(HTTP_USER_AGENT_HEADER, ''),
                ip_address=request.META.get(HTTP_IP_ADDRESS_HEADER, ''),
            )
        token.confirm_reset_pass_send_email()
        return Response({'detail': 'Ссылка отправлена', 'email': email})


class PasswordResetCheckView(PublicMixin, APIView):
    @swagger_auto_schema(operation_summary='Проверить токен сброса пароля', tags=['Регистрация и аутентификация'])
    def post(self, request, token):
        token_obj = get_object_or_404(ResetPasswordToken, key=token)
        return Response({'token': token_obj.key})


class PasswordResetConfirmView(PublicMixin, GenericAPIView):
    serializer_class = PasswordSerializer

    @swagger_auto_schema(operation_summary='Сбросить пароль', tags=['Регистрация и аутентификация'])
    def post(self, request, token):
        token_obj = get_object_or_404(ResetPasswordToken, key=token)
        user = token_obj.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data['password']
        user.set_password(password)
        user.save()
        user.pass_rst_token.all().delete()
        return Response({'detail': 'Пароль сброшен'})

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegistrationSerializer, ActivationSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema



class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer)
    def post(self, request):
        serializers = ActivationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.activate()
        return Response('Аккаунт успешно активирован', status=200)
    
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        # print('===================')
        # print(request.user)
        # print('===========================')
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы успешно вышли из своего аккаунта'
        )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(sefl, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно изменен')

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.gen_new_password()
        return Response('Новый пароль отправлен вам на почту')
    
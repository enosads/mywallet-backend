from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django_filters import rest_framework as django_filters
from rest_framework import status, permissions, viewsets
from rest_framework import views as rest_api_views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api import serializers, models


class LoginAPI(rest_api_views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, ):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user=user)
                user = user.usuario
                data = {}
                data.update(serializers.UsuarioSerializer(
                    instance=user, context={'request': request}).data),
                response = Response(data, status=status.HTTP_200_OK)
            elif User.objects.filter(username=username).count() > 0:
                data = {"error": 'Senha inválida'}
                response = Response(data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                data = {
                    "error": 'Nome de usuário inválido'}
                response = Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = {
                "error": 'Não foi possível fazer login'}
            response = Response(data, status=status.HTTP_404_NOT_FOUND)

        return response


class LoginPorTokenAPI(rest_api_views.APIView):
    def get(self, request, ):
        usuario = request.user
        if usuario:
            usuario = usuario.user
            data = {}
            data.update(serializers.UsuarioSerializer(
                instance=usuario, context={'request': request}).data),
            response = Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                "error": 'Não foi possível fazer login'}
            response = Response(data, status=status.HTTP_404_NOT_FOUND)

        return response


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.Account.objects.all()
    filter_backends = (django_filters.DjangoFilterBackend,)
    filter_fields = '__all__'

    def get_queryset(self):
        return self.queryset.filter(usuario__user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (django_filters.DjangoFilterBackend,)
    filter_fields = '__all__'

    def get_queryset(self):
        return self.queryset.filter(
            account__usuario__user=self.request.user)


class CreateUsuarioAPI(rest_api_views.APIView):
    permission_classes = [permissions.AllowAny, ]

    @transaction.atomic
    def post(self, request, ):
        try:
            serializer = serializers.CreateUsuarioSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                username = data.get('username')
                password = data.get('password')
                name = data.get('name')
                email = data.get('email')

                quantidade_de_caracteres_minimo = 8
                if len(password) < quantidade_de_caracteres_minimo:
                    raise ValidationError(
                        "Sua senha deve ter no mínimo 8 caracteres")
                user = User.objects.create_user(username, email, password)
                models.Usuario.objects.create(
                    user=user,
                    name=name,
                    email=email,
                )
                return Response(status=status.HTTP_201_CREATED)
            else:
                error = serializer.errors

        except IntegrityError:
            error = "Nome de usuário não disponível"
        except Exception as e:
            error = str(e)
        return Response({'error': error, }, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from api import serializers


class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, ):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data.get('username')
            password = data.get('password')
            usuario = authenticate(username=email, password=password)
            if usuario:
                login(request, user=usuario)
                usuario = usuario.user
                data = {}
                data.update(serializers.UsuarioSerializer(
                    instance=usuario, context={'request': request}).data),
                response = Response(data, status=status.HTTP_200_OK)
            elif User.objects.filter(username=email).count() > 0:

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


class LoginPorTokenAPI(APIView):

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

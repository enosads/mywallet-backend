from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import Usuario


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UsuarioSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, instance):
        return instance.user.username

    def get_token(self, instance):
        token, created = Token.objects.get_or_create(user=instance.user)
        return token.key

    class Meta:
        model = Usuario
        exclude = ['user']

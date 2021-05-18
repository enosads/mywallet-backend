from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api import models
from api.models import Usuario


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CreateUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = Usuario
        exclude = ['user']


class UsuarioSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Usuario
        exclude = ['user']

    def get_username(self, instance):
        return instance.user.username

    def get_token(self, instance):
        token, created = Token.objects.get_or_create(user=instance.user)
        return token.key


class AccountSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    entradas = serializers.SerializerMethodField()
    saidas = serializers.SerializerMethodField()

    class Meta:
        model = models.Account
        exclude = ['usuario']

    def get_total(self, instance):
        return instance.total()

    def get_entradas(self, instance):
        return instance.entradas()

    def get_saidas(self, instance):
        return instance.saidas()

    def create(self, validated_data):
        usuario = self.context.get('request').user.usuario
        return models.Account.objects.create(
            **validated_data, usuario=usuario)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        exclude = ['account']

    account_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Account.objects.all(),
        write_only=True, source='account')

    def create(self, validated_data):
        return models.Transaction.objects.create(
            **validated_data, )

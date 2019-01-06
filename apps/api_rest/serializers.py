from rest_framework import serializers
from .utils import validateEmail

from apps.default.models import Usuario


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class RegisterSerializer(serializers.Serializer):
    nome_completo = serializers.CharField(required=True, max_length=100)
    email = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class ConvertTokenSerializer(serializers.Serializer):
    key = serializers.CharField(required=True, max_length=100)


class AppRegistration(serializers.Serializer):
    registration_id = serializers.CharField(required=True, max_length=100)


class CotacaoSeguroSerializer(serializers.Serializer):
    valor_bike = serializers.DecimalField(max_digits=14, decimal_places=2)

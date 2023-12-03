from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_moderator')


class BankServicesSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = BankServices
        # Поля, которые мы сериализуем
        fields = '__all__'


class RequestsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, many=False)
    BankServices = serializers.SerializerMethodField()

    def get_BankServices(self, MyRequest):
        RSs = RequestsServices.objects.filter(Request=MyRequest)
        return BankServicesSerializer([rs.BankService for rs in RSs], many=True).data

    class Meta:
        # Модель, которую мы сериализуем
        model = Requests
        # Поля, которые мы сериализуем
        fields = '__all__'


class ConfOfFinesSerializer(serializers.ModelSerializer):
    BankServices = BankServicesSerializer(read_only=True, many=False)
    Request = RequestsSerializer(read_only=True, many=False)

    class Meta:
        # Модель, которую мы сериализуем
        model = RequestsServices
        # Поля, которые мы сериализуем
        fields = '__all__'


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
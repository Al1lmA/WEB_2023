from .models import *
from rest_framework import serializers

class BankServicesSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = BankServices
        # Поля, которые мы сериализуем
        fields = ["bank_service_id", "title", "button_text", "short_description", "description", "img", "order_img", "service_status"]

class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Requests
        # Поля, которые мы сериализуем
        fields = ["request_id", "request_status", "creation_date", "formation_date", "completion_date", "user", "admin"]

class RequestsServicesSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = RequestsServices
        # Поля, которые мы сериализуем
        fields = ["bank_service_id", "request_id", "bill", "rs_id"]

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Users
        # Поля, которые мы сериализуем
        fields = ["user_id", "name", "surname", "password", "phone_number", "admin_flag"]

class ManyToManySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestsServices
        fields = ["bill", "bank_service_id"]

class ServiceForRequest(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = BankServices
        # Поля, которые мы сериализуем
        fields = ["title", "button_text", "short_description", "description"]
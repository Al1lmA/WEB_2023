from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from drf_yasg.utils import swagger_auto_schema # type: ignore
from datetime import timedelta

import uuid
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT

import redis # type: ignore
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
from bmstu_lab.permissions import *



class UserViewSet(ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    model_class = Users

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAdmin | IsModerator]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def create(self, request):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request Userlogin ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(login=request.data['login']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.model_class.objects.create_user(login=serializer.data['login'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'],
                                     admin_flag=serializer.data['admin_flag'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])
@csrf_exempt
@swagger_auto_schema(method='post', request_body=UsersSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    login = request.data["login"]
    password = request.data["password"]
    user = authenticate(request, login=login, password=password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, login)

        data = {
            "session_id": random_key,
            "user_id": user.pk,
            "login": user.login,
            "admin_flag": user.admin_flag
        }

        response = Response(data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, httponly=False, expires=timedelta(days = 1))

        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")

@authentication_classes([])
@csrf_exempt
@swagger_auto_schema(method='post')
@api_view(['Post'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        ssid = request.COOKIES["session_id"]
    except:
        return HttpResponse("{'status': 'error', 'error': 'logout failed'}")
        
    session_storage.delete(ssid)

    logout(request._request)
    response = HttpResponse("{'status': 'ok'}")
    response.delete_cookie("session_id")
    return response

@api_view(['Post'])
@permission_classes([AllowAny])
def check(request):
    session_id = request.headers.get("authorization")
    print(session_id)

    print(session_storage.get(session_id))

    if (session_storage.get(session_id)):
        user = Users.objects.get(login=session_storage.get(session_id).decode('utf-8'))
        
        serializer = UsersSerializer(user, many=False)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)

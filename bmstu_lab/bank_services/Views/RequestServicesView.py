from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *

from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.views import APIView
from rest_framework.permissions import *
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT
from bmstu_lab.permissions import *
from drf_yasg.utils import swagger_auto_schema # type: ignore
import redis # type: ignore
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

class Requests_Services_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # удаление штрафа из нарушения
    # можно только если авторизован
    @swagger_auto_schema(request_body=ManyToManySerializer)
    def delete(self, request, pk, format=None):
        """
        Удаление из заявки м-м
        """
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        
        userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id
        Request = Requests.objects.filter(user=userId, request_status='черновик')
        if Request.exists():
            Request_id = Request[0].request_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        r_s = RequestsServices.objects.filter(bank_service_id=pk).filter(request_id=Request_id)

        if len(r_s) > 0:
            r_s[0].delete()

            if len(RequestsServices.objects.filter(request_id=Request_id)) == 0:
                Requests.objects.get(request_id=Request_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)



    # изменение описания штрафа
    # можно только если авторизован
    @swagger_auto_schema(request_body=ManyToManySerializer)
    def put(self, request, pk, format=None):
        """
        Изменение значения м-м
        """
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        
        userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id
        Request = Requests.objects.filter(user=userId, request_status='черновик')
        if Request.exists():
            Request_id = Request[0].request_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        r_s = RequestsServices.objects.filter(bank_service_id=pk).filter(request_id=Request_id)

        if len(r_s) > 0:
            r_s[0].bill = request.data['bill']
            r_s[0].save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
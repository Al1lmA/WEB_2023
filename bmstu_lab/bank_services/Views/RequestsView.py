from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
from datetime import datetime
from ..minio.minioClass import *

from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.views import APIView
from rest_framework.permissions import *
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT
from bmstu_lab.permissions import *
from drf_yasg.utils import swagger_auto_schema # type: ignore
import redis # type: ignore
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def checkStatus(old_status, new_status, admin):
    return ((not admin) and (new_status in ['сформирован', 'удалён']) and (old_status == 'черновик')) or (admin and (new_status in ['завершён', 'отклонён']) and (old_status == 'сформирован')) 

def getServiceWithImage(serializer: ManyToManySerializer, title):
    minio = MinioClass()
    ServiceData = serializer.data
    ServiceData['image'] = minio.getImage('bankservices', title)
    return ServiceData

def getServicesForOneRequest(serializer: ManyToManySerializer):
    ServiceList = []
    for service in serializer.data:
        Service = get_object_or_404(BankServices, bank_service_id=service['bank_service_id'])
        ServiceData = service
        ServiceData['service_data'] = getServiceWithImage(ServiceForRequest(Service), Service.title)
        ServiceList.append(ServiceData)
    return ServiceList


class Requests_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение списка заказов
    # можно только если авторизован
    def get(self, request, format=None):
        """
        Возвращает список заявок
        """
        
        RequestsFilteredList = RequestsFilter(Requests.objects.all(), request)
        serializer = RequestsSerializer(RequestsFilteredList, many=True)

        RequestData = serializer.data

        for i, obj in enumerate(serializer.data):
            user = get_object_or_404(Users, user_id=obj.get('user'))
            RequestData[i]['user_login'] = user.login
            
        return Response(RequestData, status=status.HTTP_202_ACCEPTED)
    
    # отправка заказа пользователем
    # можно только если авторизован
    @swagger_auto_schema(request_body=RequestsSerializer)
    def put(self, request, format=None):
        """
        Формирует заявку
        """
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id

        User = get_object_or_404(Users, user_id=userId)
        Request = get_object_or_404(Requests, user=userId, request_status='черновик')
        new_status = "сформирован"
        print(Request.request_status)   

        if checkStatus(Request.request_status, new_status, User.admin_flag): 
            Request.request_status = new_status
            Request.formation_date = datetime.now()
            Request.save()
            serializer = RequestsSerializer(Request)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)         
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # удаление заказа пользователем
    # можно только если авторизован
    def delete(self, request, format=None):
        """
        Удаляет заявку
        """
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id

        User = Users.objects.get(user_id=userId)
        Request = Requests.objects.filter(user=userId).filter(request_status='черновик')

        if Request.exists():
            RequestId = Request[0].request_id

        NeedRS = RequestsServices.objects.filter(request_id=RequestId)        

        if checkStatus(Request.request_status, "удалён", User.admin_flag):
            for obj in NeedRS:
                obj.delete()
                
            Request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)        
        return Response(status=status.HTTP_400_BAD_REQUEST)

        



class Request_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение нарушения
    # можно получить нарушение  если авторизован
    # если авторизован и модератор, то можно получить любой заказ
    def get(self, request, pk, format=None):
        """
        Возвращает одну заявку
        """
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        User = Users.objects.get(login=session_storage.get(ssid).decode('utf-8'))
        requests = Users.objects.filter(user=User.user_id).values_list('request_id', flat=True)

        if(pk in requests) or User.admin_flag: 

            Request = get_object_or_404(Requests, request_id=pk)
            serializer = RequestsSerializer(Request)

            positions = RequestsServices.objects.filter(request_id=pk)
            positionsSerializer = ManyToManySerializer(positions, many=True)

            response = serializer.data
            response['user_login'] = Users.objects.get(user_id=response['user']).login
            response["request's services"] = getServicesForOneRequest(positionsSerializer)
            return Response(response, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    
    # перевод заказа модератором на статус A или W
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    @swagger_auto_schema(request_body=RequestsSerializer)
    def put(self, request, pk, format=None):
        """
        Принимает или отклоняет заявку
        """
        Request = get_object_or_404(Requests, request_id=pk)
        
        try: 
            new_status = request.data['request_status']
            print(new_status)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if checkStatus(Request.request_status, new_status, True):
            Request.request_status = new_status
            Request.completion_date = datetime.now()
            Request.save()
            serializer = RequestsSerializer(Request)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    


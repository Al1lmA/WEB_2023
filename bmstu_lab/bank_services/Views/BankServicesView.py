from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
from ..minio.minioClass import *
from datetime import datetime

from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.views import APIView
from rest_framework.permissions import *
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT
from bmstu_lab.permissions import *
from drf_yasg.utils import swagger_auto_schema # type: ignore
import redis # type: ignore
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def getServiceWithImage(serializer: BankServicesSerializer):
    minio = MinioClass()
    ServiceData = serializer.data
    ServiceData.update({'image': minio.getImage('bankservices', serializer.data['title'])})
    return ServiceData

def postServiceImage(serializer: BankServicesSerializer):
    minio = MinioClass()
    minio.addImage('bankservices', serializer.data['title'], serializer.data['img'])

def putServiceImage(serializer: BankServicesSerializer, old_title):
    minio = MinioClass()
    minio.removeImage('bankservices', old_title)
    minio.addImage('bankservices', serializer.data['title'], serializer.data['img'])


class Services_View(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение списка услуг
    # можно всем
    def get(self, request, format=None):
        """
        Возвращает список услуг
        """
        try:
            ssid = request.COOKIES["session_id"]
            userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id
        except:
            userId = -1
        
        Request = Requests.objects.filter(user_id = userId).filter(request_status = 'черновик') 
        if Request.exists():
            Request_id = Request[0].request_id
        else:
            Request_id = 'null'

        CurrentList = {
            'request_id': Request_id
        }
        
        ServicesFilteredList = ServicesFilter(BankServices.objects.filter(service_status='действует'), request)
        ServicesFilteredListData = [getServiceWithImage(BankServicesSerializer(Service)) for Service in ServicesFilteredList]
        # serializer = BankServicesSerializer(ServicesFilteredList, many=True)
        CurrentList['services_list'] =  ServicesFilteredListData
        return Response(CurrentList)
    
    
    # добавление услуги
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    @swagger_auto_schema(request_body=BankServicesSerializer)
    def post(self, request, format=None):
        """
        Добавляет новую услугу
        """

        Service = BankServices.objects.filter(title=request.data['title'])
        if Service.exists():
            return Response('Такая услуга уже существует', status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BankServicesSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            postServiceImage(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Service_View(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    # получение услуги
    # можно всем
    def get(self, request, pk, format=None):
        """
        Возвращает одну услугу
        """

        Service = get_object_or_404(BankServices, bank_service_id=pk)
        serializer = BankServicesSerializer(Service)
        return Response(getServiceWithImage(serializer), status=status.HTTP_202_ACCEPTED)
        
    
    # изменение услуги
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    @swagger_auto_schema(request_body=BankServicesSerializer)
    def put(self, request, pk, format=None):
        """
        Обновляет информацию об услуге
        """
        fields = request.data

        if request.data.get('service_status'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        Service = get_object_or_404(BankServices, bank_service_id=pk)
        old_title = Service.title
        serializer = BankServicesSerializer(Service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            putServiceImage(serializer, old_title)

            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # логическое удаление услуги
    # можно только если авторизован и модератор
    @method_permission_classes((IsModerator,))
    def delete(self, request, pk, format=None):
        """
        Удаляет услугу
        """  

        Service = get_object_or_404(BankServices, bank_service_id=pk)
        Service.service_status = 'удалён'
        Service.save()
        serializer = BankServicesSerializer(Service)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    # добавление продукта в заказ
    # можно только если авторизован
    def post(self, request, pk, format=None):
        """
        Добавляет услугу в заявку
        """ 
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

        userId = Users.objects.get(login=session_storage.get(ssid).decode('utf-8')).user_id
        
        Request = Requests.objects.filter(user_id = userId).filter(request_status = 'черновик') 
        
        if not Request.exists():
            RequestNew = {
                'user': userId,
                'moder_id': 1,
                'creation_date': datetime.now(),
            }
            RequestSerializer = RequestsSerializer(data=RequestNew)

            if not RequestSerializer.is_valid():
                return Response(RequestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            RequestSerializer.save()
        
        
        NewRequest = Requests.objects.filter(user_id = userId).filter(request_status = 'черновик') 
        Request_id = NewRequest[0].request_id

        if Requests.objects.get(request_id=Request_id).request_status != 'черновик' or RequestsServices.objects.filter(bank_service_id=pk).filter(request_id=Request_id).exists():
            return Response({'error': 'Услуга уже добавлена в заявку'}, status=status.HTTP_400_BAD_REQUEST)
        
        NewRS = {
            'bank_service_id': pk,
            'request_id': Request_id,
            'bill': 'New number',
        }
        serializer = RequestsServicesSerializer(data=NewRS)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
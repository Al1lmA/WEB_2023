from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
from ..minio.minioClass import *
# Create your views here.

def getServiceWithImage(serializer: BankServicesSerializer):
    minio = MinioClass()
    ServiceData = serializer.data
    ServiceData['image'] = minio.getImage('bankservices', serializer.data['bank_service_id'], serializer.data['img'])
    return ServiceData

def postServiceImage(request, serializer: BankServicesSerializer):
    minio = MinioClass()
    minio.addImage('bankservices', serializer.data['bank_service_id'], request.data['image'], serializer.data['img'])

def putServiceImage(request, serializer: BankServicesSerializer):
    minio = MinioClass()
    minio.removeImage('bankservices', serializer.data['bank_service_id'], serializer.data['picture'])
    minio.addImage('bankservices', serializer.data['bank_service_id'], request.data['image'], serializer.data['img'])

def GetUser():
    return 2


@api_view(['Get','Post'])
def services_list_form(request, format=None):
    if request.method == 'GET':
        """
        Возвращает список услуг
        """

        ServicesFilteredList = ServicesFilter(BankServices.objects.filter(service_status='действует'), request)
        ServicesFilteredListData = [getServiceWithImage(BankServicesSerializer(Service)) for Service in ServicesFilteredList]
        # serializer = BankServicesSerializer(ServicesFilteredList, many=True)
        return Response(ServicesFilteredListData)
    
    elif request.method == 'POST':
        """
        Добавляет новую услугу
        """

        serializer = BankServicesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            postServiceImage(request, serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['Get', 'Put', 'Delete', 'Post'])
def services_detail(request, pk, format=None):
    if request.method == 'GET':
        """
        Возвращает одну услугу
        """

        Service = get_object_or_404(BankServices, service_id=pk)
        serializer = BankServicesSerializer(Service)
        return Response(getServiceWithImage(serializer), status=status.HTTP_202_ACCEPTED)
        
    elif request.method == 'PUT':
        """
        Обновляет информацию об услуге
        """
        # fields = request.data.keys()

        if request.data.get('service_status'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        Service = get_object_or_404(BankServices, service_id=pk)
        serializer = BankServicesSerializer(Service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # if 'image' in fields:
            #     putServiceImage(request, serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Удаляет услугу
        """  

        Service = get_object_or_404(BankServices, service_status=pk)
        Service.service_status = request.data['service_status']
        Service.save()
        serializer = BankServicesSerializer(Service)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'POST':
        """
        Добавляет услугу в заявку
        """ 

        userId = GetUser()
        Request = Requests.objects.filter(user=userId, request_status='черновик')
        Request_id = Request.request_id
        if len(Request) == 0:
            Request_new = {}
            Request_new['user'] = userId
            Request_new['admin'] = 1
            serializer = RequestsSerializer(data=Request_new)

            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        if (Request.objects.get(request_id=Request_id).status != 'черновик') or (len(RequestsServices.objects.filter(bank_service_id=pk).filter(Request_id=Request_id)) != 0):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        r_s_new = {}
        r_s_new['sbank_service_id'] = pk
        r_s_new['request_id'] = Request_id
        r_s_new['bill'] = 'bill number (in future)'

        serializer = ManyToManySerializer(data=r_s_new)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
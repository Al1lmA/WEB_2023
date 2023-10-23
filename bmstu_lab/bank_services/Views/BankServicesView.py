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

# def getFineWithImage(serializer):
#     minio = MinioClass()
#     FineData = serializer.data
#     FineData['image'] = minio.getImage('fines', serializer.data['fine_id'], serializer.data['picture'])
#     return FineData

# def postFineImage(request, serializer: FinesSerializer):
#     minio = MinioClass()
#     minio.addImage('fines', serializer.data['fine_id'], request.data['image'], serializer.data['picture'])

# def putFineImage(request, serializer: FinesSerializer):
#     minio = MinioClass()
#     minio.removeImage('fines', serializer.data['fine_id'], serializer.data['picture'])
#     minio.addImage('fines', serializer.data['fine_id'], request.data['image'], serializer.data['picture'])

def GetUser():
    return 2


@api_view(['Get','Post'])
def services_list_form(request, format=None):
    if request.method == 'GET':
        """
        Возвращает список услуг
        """

        # print('get')

        ServicesFilteredList = ServicesFilter(BankServices.objects.filter(service_status='действует'), request)
        # FinesListData = [getFineWithImage(FinesSerializer(Fine)) for Fine in FinesList]
        serializer = BankServicesSerializer(ServicesFilteredList, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        """
        Добавляет новую услугу
        """

        # print('post')

        serializer = BankServicesSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['Get', 'Put', 'Delete', 'Post'])
def services_detail(request, pk, format=None):
    if request.method == 'GET':
        """
        Возвращает одну услугу
        """

        Service = get_object_or_404(BankServices, service_id=pk)

        if request.method == 'GET':
            serializer = BankServicesSerializer(Service)
            return Response(serializer.data)
        
    elif request.method == 'PUT':
        """
        Обновляет информацию об услуге
        """

        if request.data.get('service_status'):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        Service = get_object_or_404(BankServices, service_id=pk)
        serializer = BankServicesSerializer(Service, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
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
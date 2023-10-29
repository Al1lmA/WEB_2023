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


@api_view(['Get','Post'])
def services_list_form(request, format=None):
    if request.method == 'GET':
        """
        Возвращает список услуг
        """
        userId = 2
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
    
    elif request.method == 'POST':
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

    elif request.method == 'DELETE':
        """
        Удаляет услугу
        """  

        Service = get_object_or_404(BankServices, bank_service_id=pk)
        Service.service_status = 'удалён'
        Service.save()
        serializer = BankServicesSerializer(Service)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'POST':
        """
        Добавляет услугу в заявку
        """ 

        userId = 3
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
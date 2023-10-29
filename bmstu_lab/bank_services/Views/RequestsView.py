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


@api_view(['Get', 'Put', 'Delete'])
def request_list_form(request, format=None):
    if request.method == 'GET':
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
    

    elif request.method == 'PUT':
        """
        Формирует заявку
        """

        userId = 2
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
    
    elif request.method == 'DELETE':
        """
        Удаляет заявку
        """

        userId = 2
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


@api_view(['Get', 'Put'])
def request_detail(request, pk, format=None):
    if request.method == 'GET':
        """
        Возвращает одну заявку
        """

        Request = get_object_or_404(Requests, request_id=pk)
        serializer = RequestsSerializer(Request)

        positions = RequestsServices.objects.filter(request_id=pk)
        positionsSerializer = ManyToManySerializer(positions, many=True)

        response = serializer.data
        response['user_login'] = Users.objects.get(user_id=response['user']).login
        response["request's services"] = getServicesForOneRequest(positionsSerializer)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    
    elif request.method == 'PUT':
        """
        Изменяет заявку
        """

        Request = get_object_or_404(Requests, request_id=pk)
        serializer = RequestsSerializer(Request, data=request.data)

        if 'status' in request.data.keys():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['Put'])
def request_final(request, pk, format=None):
        """
        Принимает или отклоняет заявку
        """

        userId = 1
        User = get_object_or_404(Users, user_id=userId)
        Request = get_object_or_404(Requests, request_id=pk)


        try: 
            new_status = request.data['request_status']
            print(new_status)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        if checkStatus(Request.request_status, new_status, User.admin_flag):
            Request.request_status = new_status
            Request.completion_date = datetime.now()
            Request.save()
            serializer = RequestsSerializer(Request)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)        
        return Response(status=status.HTTP_400_BAD_REQUEST)
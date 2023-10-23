from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
from datetime import datetime
# Create your views here.

def checkStatus(old_status, new_status, admin):
    return ((not admin) and (new_status in ['сформирован', 'удалён']) and (old_status == 'черновик')) or (admin and (new_status in ['завершён', 'отклонён']) and (old_status == 'сформирован')) 

def GetUser():
    return 2

@api_view(['Get','Put'])
def request_list_form(request, format=None):
    if request.method == 'GET':
        """
        Возвращает список заявок
        """
        
        RequestsFilteredList = RequestsFilter(Requests.objects.all(), request)
        serializer = RequestsSerializer(RequestsFilteredList, many=True)
        return Response(serializer.data)
    

    elif request.method == 'PUT':
        """
        Формирует заявку
        """
        userId = GetUser()
        User = get_object_or_404(Users, user_id=userId)
        Request = get_object_or_404(Requests, user=userId, request_status='черновик')
        new_status = "сформирован"
        print(Request.request_status)   

        if checkStatus(Request.request_status, new_status, User.admin_flag): 
            print("hi")                        
            Request.request_status = new_status
            Request.formation_date = datetime.now()
            Request.save()
            serializer = RequestsSerializer(Request)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
         
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['Get','Put','Delete'])
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
        response['positions'] = positionsSerializer.data
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
    
    elif request.method == 'DELETE':
        """
        Удаляет заявку
        """

        userId = GetUser()
        User = Users.objects.get(user_id=userId)
        Request = get_object_or_404(Requests, user=userId, requests_status='черновик')

        if checkStatus(Request.request_status, "удалён", User.admin_flag):
            Request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    
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
            print(new_status)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
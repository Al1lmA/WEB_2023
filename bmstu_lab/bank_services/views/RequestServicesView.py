from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from ..serializers import *
from ..models import *
from rest_framework.decorators import api_view
from ..filters import *
# Create your views here.

def GetUser():
    return 2

@api_view(['Put','Delete'])
def Change_Fine(request, pk, format=None):

    userId = GetUser()
    Request = Requests.objects.filter(user=userId, request_status='черновик')
    Request_id = Request.request_id
    r_s = RequestsServices.objects.filter(bank_service_id=pk).filter(request_id=Request_id)

    if request.method == 'DELETE':
        if len(r_s) > 0:
            r_s[0].delete()

            if len(RequestsServices.objects.filter(request_id=Request_id)) == 0:
                Requests.objects.get(request_id=Request_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        if len(r_s) > 0:
            r_s[0].bill = request.data['bill']
            r_s[0].save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
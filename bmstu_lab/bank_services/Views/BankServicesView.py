from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response

from .RequestsView import find_draft_request
from ..serializers import *
from ..models import *

from bmstu_lab.permissions import *
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT
import redis

from ..utils import get_session

session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


@api_view(["GET"])
def services(request):
    query = request.GET.get("title", "")
    bankServices = BankServices.objects.filter(title__icontains=query)
    draft_Request = find_draft_request(request)


    data = {
        "request_id": draft_Request.id if draft_Request else None,
        "services": BankServicesSerializer(bankServices, many=True).data
    }

    return Response(data)


@api_view(["GET"])
def search_services(request):
    query = request.GET.get("title", "")
    bankServices = BankServices.objects.filter(title__icontains=query, status=1)
    draft_Request = find_draft_request(request)


    data = {
        "request_id": draft_Request.id if draft_Request else None,
        "services": BankServicesSerializer(bankServices, many=True).data
    }

    return Response(data)


@api_view(["GET"])
def get_service(request, service_id):
    BankService = BankServices.objects.get(pk=service_id)
    serializer = BankServicesSerializer(BankService, many=False)

    return Response(serializer.data)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def edit_service(request, service_id):

    session_id = get_session(request)
    if session_id is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    user = CustomUser.objects.get(username=session_storage.get(session_id).decode('utf-8'))
    if not user.is_moderator:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    service = BankServices.objects.get(pk=service_id)

    fields = request.data.keys()
    if 'pk' in fields:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = BankServicesSerializer(service, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_service(request):
    print(request.data)
    session_id = get_session(request)
    if session_id is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    user = CustomUser.objects.get(username=session_storage.get(session_id).decode('utf-8'))    
    if not user.is_moderator:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    fields = request.data.keys()
    if 'pk' in fields:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer = BankServicesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_service_to_request(request, service_id):
    session_id = get_session(request)
    # print(session_id)
    user = CustomUser.objects.get(username=session_storage.get(session_id).decode('utf-8'))

    draft_request = find_draft_request(request)


    if draft_request is None:
        draft_request = Requests.objects.create()
        draft_request.user = user
        draft_request.save()

    if RequestsServices.objects.filter(Request_id=draft_request.pk, BankService_id=service_id):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = RequestsServices.objects.create()
    cons.Request = draft_request
    cons.BankService = BankServices.objects.get(pk=service_id)
    cons.save()


    serializer = RequestsSerializer(draft_request, many=False)
    
    return Response(serializer.data, status=status.HTTP_200_OK)

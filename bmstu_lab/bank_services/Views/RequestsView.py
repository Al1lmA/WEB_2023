from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *


from bmstu_lab.permissions import *
from rest_framework.decorators import permission_classes, api_view
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT
import redis

from ..utils import get_session

session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_requests(request):
    session_id = get_session(request)

    user = CustomUser.objects.get(username=session_storage.get(session_id).decode('utf-8'))

    requests = Requests.objects.filter(user_id=user.pk)

    serializer = RequestsSerializer(requests, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_draft_request(request):
    draft_request = find_draft_request(request)

    if draft_request is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RequestsSerializer(draft_request, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_servce_from_request(request, request_id, service_id):
    if not RequestsServices.objects.filter(Request_id=request_id, BankService_id=service_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    conf = RequestsServices.objects.get(Request_id=request_id, BankService_id=service_id)
    conf.delete()

    Request = Requests.objects.get(pk=request_id)
    serializer = RequestsSerializer(Request, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_request(request, request_id):
    if not Requests.objects.filter(pk=request_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    for conf in RequestsServices.objects.filter(Request_id=request_id):
        conf.delete()

    Request = Requests.objects.get(pk=request_id)
    Request.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_request_status_user(reques, request_id):
    if not Requests.objects.filter(pk=request_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    Request = Requests.objects.get(pk=request_id)
    Request.status = 2
    Request.formated_date = datetime.now(tz=timezone.utc)
    Request.save()

    return Response(status=status.HTTP_200_OK)


def find_draft_request(request):
    session_id = get_session(request)
    
    if session_id is None:
        return None
    
    if session_id not in session_storage:
        return None

    user = CustomUser.objects.get(username=session_storage.get(session_id).decode('utf-8'))

    Request = Requests.objects.filter(user_id=user.pk).filter(status=1).first()

    # print(Request)

    if Request is None:
        return None

    return Request
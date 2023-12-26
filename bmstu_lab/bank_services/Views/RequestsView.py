from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from ..serializers import *
from ..models import *

from bmstu_lab.permissions import *
from rest_framework.decorators import permission_classes, api_view
from bmstu_lab.settings import REDIS_HOST, REDIS_PORT, PASSWORD_ACYNC
import redis
import requests

from ..utils import get_session

session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_requests(request):
    session_id = get_session(request)
    user = get_object_or_404(CustomUser, username=session_storage.get(session_id).decode('utf-8'))

    if user.is_moderator == True:
        requests = Requests.objects.all()
    else: 
        requests = Requests.objects.filter(user_id=user.pk)

    # Get parameters for date range and status from the request
    start_date = request.query_params.get('start_date', None)
    end_date = request.query_params.get('end_date', None)
    status = request.query_params.get('status', None)

     # Parse start_date and end_date and filter the query if they are provided
    if start_date:
        requests = requests.filter(formated_date__gte=start_date)

    if end_date:
            requests = requests.filter(formated_date__lte=end_date)

    # If status parameter is provided, filter by the status
    if status:
        try:
            status_num = int(status)
            if status_num in dict(Requests.STATUS_CHOICES).keys():
                requests = requests.filter(status=status_num)
        except ValueError:
            pass  # or you could return an error message that status must be an integer


    print(start_date)

    # Serialize and return response
    serializer = RequestsSerializer(requests, many=True)
    # print(serializer.data)
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
def update_request_status_user(request):

    Request = find_draft_request(request)
    Request.status = 2

    url = "http://127.0.0.1:5000/rating/"
    params = { "request_id" : Request.pk }
    response = requests.post(url, json=params)
    print(response.status_code)

    Request.formated_date = datetime.now(tz=timezone.utc)
    Request.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_request_status_admin(request, request_id):
    session_id = get_session(request)
    user = get_object_or_404(CustomUser, username=session_storage.get(session_id).decode('utf-8'))
    print(user)
    print(request.data)

    if not user.is_moderator == True:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    Request = Requests.objects.get(pk=request_id)
    Request.status = request.data['status']
    Request.closed_date = datetime.now()
    Request.save()
    serializer = RequestsSerializer(Request)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(["PUT"])
def rating(request, request_id):
    rating = request.data["rating"]
    password = request.data["password"]
    print(rating, password)
    if password != PASSWORD_ACYNC:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        Request = Requests.objects.get(pk=request_id)
        Request.rating = rating
        print(Request.rating)
        Request.save()
        return Response(status=status.HTTP_200_OK)
    
    except Requests.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



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
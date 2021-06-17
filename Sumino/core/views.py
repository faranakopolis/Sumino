""" This module includes the Sumino's views.

Here are the functions and general logic of the project.

"""
import datetime

from django.db.models import Sum, F
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, OR
from rest_framework.response import Response

from Sumino.core.models import Number
from Sumino.core.serializers import SumSerializer
from Sumino.redisDriver.utils import *
from Sumino.core.permissions import UserIsBlockedPermission, UserIsSumBlockedPermission


# Functions
def get_duration():
    # Calculate the expiration time in which the user can request in a specific range

    now = datetime.datetime.now().replace()

    hours_added = datetime.timedelta(hours=1)

    next_hour = now + hours_added
    next_hour = next_hour.replace(minute=0, second=0)

    duration = (next_hour - now).total_seconds()

    return int(duration)


# I had to specify methods list in here. So, I can track and identify them inside the view.
# To make it simple, I just considered CRUD methods
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((UserIsBlockedPermission, UserIsSumBlockedPermission))
def sum_view(request, **kwargs):
    response = {}

    # Pass the inputs to the SumSerializer in order to check their formats
    serializer = SumSerializer(data=request.query_params)

    # Get the user ip
    user_ip = request.META.get('REMOTE_ADDR')

    if request.method != "GET":  # Method not allowed
        error_msg = f"Method {request.method} not allowed !!!"
        key = f"{user_ip}_wrong"
        update_user_request_count(key, expires_at=get_duration())

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # Check if the input data is well-formed
    if not serializer.is_valid():  # The input data is not well-formed

        response['response'] = {"please enter a well-format input based on this error ": serializer.errors}

        # Update bad request counts for key = user ip
        key = f"{user_ip}_wrong"
        update_user_request_count(key, expires_at=get_duration())

        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    # The request is correct
    # Update sum request counts for key = user ip
    key = f"{user_ip}_sum"
    update_user_request_count(key, expires_at=get_duration())

    # Insert a,b into the number table
    serializer.save()
    response['result'] = serializer.validated_data['a'] + serializer.validated_data['b']
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((UserIsBlockedPermission, IsAuthenticated))
def history_view(request, **kwargs):
    if request.method != "GET":  # Method not allowed

        # Get user ip
        user_ip = request.META.get('REMOTE_ADDR')

        error_msg = f"Method {request.method} not allowed !!!"
        key = f"{user_ip}_wrong"
        update_user_request_count(key, expires_at=get_duration())

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # The request is correct
    numbers_list = []
    numbers = Number.objects.all()

    for num in numbers:
        numbers_list.append({"a": num.a,
                             "b": num.b,
                             "created_at": num.created_at})

    return Response(data={"Response": numbers_list}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((UserIsBlockedPermission, IsAuthenticated))
def total_view(request, **kwargs):
    if request.method != "GET":  # Method not allowed

        # Get user ip
        user_ip = request.META.get('REMOTE_ADDR')

        error_msg = f"Method {request.method} not allowed !!!"
        key = f"{user_ip}_wrong"
        update_user_request_count(key, expires_at=get_duration())

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # The request is correct
    total = Number.objects.aggregate(total=Sum(F('a') + F('b')))["total"]

    return Response(data={"Response": total}, status=status.HTTP_200_OK)

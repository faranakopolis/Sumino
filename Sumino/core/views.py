""" This module includes the Sumino's views.

Here are the functions and general logic of the project.

"""
import datetime

from django.db.models import Sum, F
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Sumino.core.models import Number
from Sumino.core.serializers import SumSerializer
from Sumino.redisDriver.utils import *
from Sumino.core.permissions import UserIsBlockedPermission, UserIsSumBlockedPermission


# Functions
def get_duration():
    # Calculate the expiration time in which the user can request for 100 times

    now = datetime.datetime.now().replace()

    hours_added = datetime.timedelta(hours=1)

    next_hour = now + hours_added
    next_hour = next_hour.replace(minute=0, second=0)

    duration = (next_hour - now).total_seconds()

    return int(duration)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((UserIsBlockedPermission, UserIsSumBlockedPermission))
def sum_view(request, **kwargs):
    response = {}

    # Pass the inputs to the SumSerializer in order to their format checking
    serializer = SumSerializer(data=request.query_params)

    # Get User's IP
    user_ip = request.META.get('REMOTE_ADDR')

    if request.method == "GET":
        # Check if the input data is well-format
        if serializer.is_valid():
            update_user_request_count(user_ip, expires_at=get_duration(), request_type="sum")

            # Insert a,b into number table
            serializer.save()
            response['result'] = serializer.validated_data['a'] + serializer.validated_data['b']
            return Response(data=response, status=status.HTTP_200_OK)

        else:  # The input data is not well-formed

            response['response'] = {"please enter a well-format input based on this error ": serializer.errors}

            # Plus bad request counts for this user(IP)
            update_user_request_count(user_ip, expires_at=get_duration(), request_type="wrong")

            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    else:  # Method not allowed
        error_msg = "Method " + request.method + " not allowed !!!"

        update_user_request_count(user_ip, expires_at=get_duration(), request_type="wrong")

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated, UserIsBlockedPermission))
def history_view(request, **kwargs):
    if request.method == "GET":
        numbers_list = []
        numbers = Number.objects.all()

        for num in numbers:
            numbers_list.append({"a": num.a,
                                 "b": num.b,
                                 "created_at": num.created_at})

        return Response(data={"Response": numbers_list}, status=status.HTTP_200_OK)

    else:  # Method not allowed

        # Get User's IP
        user_ip = request.META.get('REMOTE_ADDR')

        error_msg = "Method " + request.method + " not allowed !!!"

        update_user_request_count(user_ip, expires_at=get_duration(), request_type="wrong")

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated, UserIsBlockedPermission))
def total_view(request, **kwargs):
    if request.method == "GET":
        total = Number.objects.aggregate(total=Sum(F('a') + F('b')))["total"]

        return Response(data={"Response": total}, status=status.HTTP_200_OK)

    else:  # Method not allowed

        # Get User's IP
        user_ip = request.META.get('REMOTE_ADDR')

        error_msg = "Method " + request.method + " not allowed !!!"

        update_user_request_count(user_ip, expires_at=get_duration(), request_type="wrong")

        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

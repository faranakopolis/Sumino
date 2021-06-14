""" This module includes the Sumino's views.

Here are the functions and general logic of the project.

"""
from datetime import datetime

from django.db.models import Sum, F
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Sumino.core.models import Number
from Sumino.core.serializers import SumSerializer
from Sumino.redisDriver.utils import *

SUM_REQUEST_LIMIT = 100
BAD_REQUEST_LIMIT = 15


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny,))
def sum_view(request, **kwargs):
    if request.method == "GET":
        response = {}

        # Pass the inputs to the SumSerializer in order to their format checking
        serializer = SumSerializer(data=request.query_params)

        # Check if the input data is well-format
        if serializer.is_valid():
            # First of all, Check the user's request limit count
            # Get User's IP
            user_ip = request.META.get('REMOTE_ADDR')

            # Update this user's sum requests limit in Redis db (ip -> counts)
            # Calculate the expiration time in which the user can request for 100 times
            now = datetime.now()
            next_hour = now.replace(hour=now.hour + 1,
                                    minute=0,
                                    second=0)
            duration = (next_hour - now).total_seconds()

            result = update_user_request_count(user_ip, expires_at=int(duration), request_type="sum")

            if result == 1:  # User request limit updated successfully
                # Insert a,b into number table
                serializer.save()
                response['result'] = serializer.validated_data['a'] + serializer.validated_data['b']
                return Response(data=response, status=status.HTTP_200_OK)

            elif result == -1:  # User exceeded its limit
                response['response'] = "Too Many Requests in one hour! you've been blocked till the next hour"
                return Response(data=response, status=status.HTTP_429_TOO_MANY_REQUESTS)

        else:  # The input data is not well-formed
            # Plus bad request counts for this user(IP)
            response['response'] = serializer.errors
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    else:  # Method not allowed
        error_msg = "Method " + request.method + " not allowed !!!"
        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated,))
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
        error_msg = "Method " + request.method + " not allowed !!!"
        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated,))
def total_view(request, **kwargs):
    if request.method == "GET":
        total = Number.objects.aggregate(total=Sum(F('a') + F('b')))["total"]

        return Response(data={"Response": total}, status=status.HTTP_200_OK)

    else:  # Method not allowed
        error_msg = "Method " + request.method + " not allowed !!!"
        return Response(data={"response": error_msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

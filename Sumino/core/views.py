""" This module includes the Sumino's views.

Here are the functions and general logic of the project.

"""
from django.db.models import Sum, F
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Sumino.core.models import Number
from Sumino.core.serializers import SumSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny,))
def sum_view(request, **kwargs):
    if request.method == "GET":
        result = {}

        # Pass the inputs to the SumSerializer in order to their format checking
        serializer = SumSerializer(data=request.query_params)

        # Check if the input data is well-format
        if serializer.is_valid():

            # Insert a,b into number table
            serializer.save()

            result['result'] = serializer.validated_data['a'] + serializer.validated_data['b']
            return Response(data=result, status=status.HTTP_200_OK)

        else:  # The input data is not well-formed
            # Plus bad request counts for this user(IP)
            result['response'] = serializer.errors
            return Response(data=result, status=status.HTTP_400_BAD_REQUEST)

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

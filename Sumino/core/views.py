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


@api_view(['GET'])
@permission_classes((AllowAny,))
def sum_view(request, **kwargs):
    a = float(request.query_params.get('a'))
    b = float(request.query_params.get('b'))

    # Insert a,b into number table
    num = Number(first=a, second=b)
    num.save()

    return Response(data={"result": a + b}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated,))
def history_view(request, **kwargs):
    numbers_list = []
    numbers = Number.objects.all()

    for num in numbers:
        numbers_list.append({"a": num.first,
                             "b": num.second,
                             "created_at": num.created_at})

    return Response(data={"Response": numbers_list}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes((IsAuthenticated,))
def total_view(request, **kwargs):
    total = Number.objects.aggregate(total=Sum(F('first') + F('second')))["total"]

    return Response(data={"Response": total}, status=status.HTTP_200_OK)

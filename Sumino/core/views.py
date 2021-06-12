""" This module includes the Sumino's views.

Here are the functions and general logic of the project.

"""

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Sumino.core.models import Number


@api_view()
def sum_view(request, **kwargs):
    if request.method == 'GET':
        a = float(request.query_params.get('a'))
        b = float(request.query_params.get('b'))

        # Insert a,b into number table
        num = Number(first=a, second=b)
        num.save()

        return Response(data={"result": a + b}, status=status.HTTP_200_OK)


@api_view()
def history_view(request, **kwargs):
    if request.method == 'GET':
        numbers_list = []
        numbers = Number.objects.all()

        for num in numbers:
            numbers_list.append({"a": num.first,
                                 "b": num.second,
                                 "created_at": num.created_at})

        return Response(data={"Response": numbers_list}, status=status.HTTP_200_OK)

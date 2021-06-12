"""This module includes all the serializers
    that is needed to make the Views tasks easier and cleaner.

"""

from rest_framework import serializers

from Sumino.core.models import *


class SumSerializer(serializers.ModelSerializer):

    # def validate(self, data):
    #     print(data)

    class Meta:
        model = Number
        fields = ('id', 'a', 'b', 'created_at')

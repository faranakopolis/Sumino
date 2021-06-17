""" This module includes the Sumino's models based on their tables in database.

"""

import datetime

from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser

from django.db import models


class Number(models.Model):
    id = models.AutoField(primary_key=True)
    a = models.FloatField(null=False)  # First number
    b = models.FloatField(null=False)  # Second number
    created_at = models.DateTimeField(default=datetime.datetime.now(), null=False)

    class Meta:
        db_table = "number"

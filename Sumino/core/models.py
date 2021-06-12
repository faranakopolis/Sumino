""" This module includes the Sumino's models
     based on the database design.

"""

import datetime

from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser

from django.db import models


class Number(models.Model):
    id = models.AutoField(primary_key=True)
    first = models.FloatField(null=False)
    second = models.FloatField(null=False)
    created_at = models.DateTimeField(default=datetime.datetime.now(), null=False)

    class Meta:
        db_table = "number"

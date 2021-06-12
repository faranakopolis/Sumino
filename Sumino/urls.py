"""Sumino
Is a simple summing system including following APIs:
    - Get sum of two numbers (a,b)
    - Get all of numbers (a,b)
    - Get the sum of total numbers

Here is Sumino URL Configuration file

Author: Maripillon (Faranak Heydari)
"""
from django.contrib import admin
from django.urls import path
import Sumino.core.views as views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sum/', views.sum_view, name='get_sum_of_inputs'),
    path('history/', views.history_view, name='get_history_of_inputs'),
]

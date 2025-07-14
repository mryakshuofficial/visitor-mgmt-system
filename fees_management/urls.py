from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from . import views

urlpatterns = [
    path('',views.fees_index,name='fees_index'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
] 
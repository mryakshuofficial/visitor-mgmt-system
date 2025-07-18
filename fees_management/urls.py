from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from . import views

urlpatterns = [
    path('',views.fees_index,name='fees_index'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
<<<<<<< HEAD
    path('fetch_student_data/<str:grno>/', views.fetch_student_data, name='fetch_student_data'),

=======
>>>>>>> b0f15a9ef4d613e18f17b81ef6b147bd47826eff
] 
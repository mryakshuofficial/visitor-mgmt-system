from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from . import views

urlpatterns = [
    path('',views.marks_index,name='marks_index'),
    path('marks_edit/<int:id>',views.marks_edit,name='marks_edit'),
    path('marks_delete/<int:id>',views.marks_delete,name='marks_delete'),
    path('marks_report/<int:id>',views.marks_report,name='marks_report'),
    path('fetch_student/<str:gr_no>/', views.fetch_student, name='fetch_student'),

] 
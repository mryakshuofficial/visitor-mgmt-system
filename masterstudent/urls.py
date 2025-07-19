from django.urls import path
from . import views

urlpatterns = [

    path('', views.student_profile_login, name='student_login'),
    path('profile/<int:gr_no>/', views.student_profile_view, name='view'),
]
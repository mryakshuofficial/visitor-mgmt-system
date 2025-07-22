from django.urls import path
from . import views

urlpatterns = [

    path('', views.student_profile_login, name='student_login'),
    path('profile/<str:gr_no>/', views.student_profile_view, name='view'),
    path('search/', views.admin_search_view, name='admin_search_view'),

]
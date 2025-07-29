from django.urls import path
from . import views

urlpatterns = [

    path('', views.student_profile_login, name='student_login'),
    path('profile/<str:gr_no>/', views.student_profile_view, name='view'),
    path('search/', views.admin_search_view, name='admin_search_view'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('download/<str:grno>/<str:filename>/', views.download_document, name='download_document'),

]
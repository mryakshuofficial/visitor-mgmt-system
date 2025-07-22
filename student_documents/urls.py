from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_document, name='upload_document'),
    path('upload-success/', views.upload_success, name='upload_success'),
]
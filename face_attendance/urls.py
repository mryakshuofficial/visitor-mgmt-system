# face_attendance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('capture/', views.capture_face, name='capture_face'),
    # path('recognize/', views.recognize_face, name='recognize'),
    path('recognize/', views.recognize_face, name='recognize_face'),
    path('confirm/', views.confirm_attendance, name='confirm_attendance'),
]

from django.urls import path
from feedback import views

urlpatterns = [
    path('', views.submit_feedback, name='submit_feedback'),
    path('view_all_feedback/', views.view_all_feedbacks, name='view_all_feedbacks'),
    path('toggle/<int:feedback_id>/', views.toggle_feedback_status, name='toggle_feedback_status'),
]
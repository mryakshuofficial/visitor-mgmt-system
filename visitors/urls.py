from django.contrib import admin
from django.urls import path, include
from visitors import views
urlpatterns = [
    path('',views.login_user,name="login"),
    path('visitors_index',views.visitors_index,name="visitors_index"),
    path('edit/<int:id>',views.edit,name="edit"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('logout_user',views.logout_user,name="logout"),
    path('export_pdf',views.export_pdf,name="export_pdf"),
]
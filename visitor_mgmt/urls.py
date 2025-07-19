"""
URL configuration for visitor_mgmt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from visitors import urls
from django.conf import settings
from django.conf.urls.static import static  
from . import views
from visitors.views import login_user, logout_user 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.dashboard,name='dashboard'),
    path('visitors/', include('visitors.urls')),
    path('marks/', include('marks.urls')),  # ✅ This makes URL path /fees/ work
    path('login/', login_user, name='login'),  # from visitors.views
    path('logout/', logout_user, name='logout'),  # from visitors.views
    path('fees/', include('fees_management.urls')),
    path('masterstudent/', include('masterstudent.urls')),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

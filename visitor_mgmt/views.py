from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
 
# Create your views here.

# @login_required  no need now
def dashboard(request):
    return render(request,'dashboard.html')

from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_notice(request):
    # custom view logic
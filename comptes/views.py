from django.shortcuts import render, redirect
from django.views.generic import ListView

def connexionview(request):
    return render(request, 'registration/login.html')
from django.shortcuts import render, redirect
from django.views.generic import ListView


class Accueille(ListView):
    template_name = 'comptes/accueille.html'



def connexionview(request):
    pass
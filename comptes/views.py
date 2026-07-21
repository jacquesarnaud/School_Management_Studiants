from django.views.generic import FormView,ListView,CreateView,FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.views import LoginView,LogoutView

from .forms import ConnexionForms

class ConnexionView(LoginView):

    template_name = "comptes/connexion.html"
    authentication_form = ConnexionForms
    redirect_authenticated_user = True

    def get_success_url(self):

        user = self.request.user

        if user.role == "admin":
            return reverse_lazy("admin_dashboard")

        elif user.role == "professeur":
            return reverse_lazy("prof_dashboard")

        elif user.role == "etudiant":
            return reverse_lazy("etu_dashboard")

        return reverse_lazy("login")

def acceuille(request):
    return render(request , 'comptes/accueil.html')
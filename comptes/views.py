from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView,FormView
from django.contrib.auth import authenticate, login,logout
from .forme import ConnexionForm


class Accueille(TemplateView):
    template_name = 'comptes/accueille.html'


class Connecter(FormView):
    template_name = "comptes/connexion.html"
    form_class = ConnexionForm

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(
            self.request,
            username=username,
            password=password
        )

        if user is None:
            form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
            return self.form_invalid(form)

        login(self.request, user)

        if user.role == "admin":
            return redirect("admin_dashboard")
        elif user.role == "professeur":
            return redirect("prof_dashboard")
        elif user.role == "etudiant":
            return redirect("etudiant_dashboard")

        return redirect("index")

def Deconnection(request):
    logout(request)
from django.views.generic import FormView,ListView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy

from .formulaire_compt import ConnexionForm


class ConnexionView(FormView):
    template_name = 'comptes/connexion.html'
    form_class = ConnexionForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        print("FORMULAIRE VALIDE")

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(
            self.request,
            username=email,
            password=password
        )

        print(user)

        if user:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "Identifiants incorrects")
        return self.form_invalid(form)

class Home(ListView):
    template_name = "comptes/home.html"


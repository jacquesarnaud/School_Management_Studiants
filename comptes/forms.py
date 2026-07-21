from django import forms
from django.contrib.auth.forms import AuthenticationForm

class ConnexionForms(AuthenticationForm):
    
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre email",
        })
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Entrez votre mot de passe",
        })
    )

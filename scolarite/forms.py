from django import forms
from .models import *

class Etudiantforms(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['nom','prenom','age','classe']



class Professeurforms(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = ['nom','prenom','age','classe','matiere']



from django.urls import path,include
from .views import *

urlpatterns = [
    path('users_liste',afficher_utilisateur,name='users_liste'),
    path('admin_dashboard',admin_dashboard,name='dashbord_admin'),
    path('ajouter_etudiant',ajouter_etudiant,name='ajouter_etudiant'),
    path('identifiant',identifiant,name='identifiant'),
    path('etudiant_dashboard',etudiant_dashboard,name='etudiant_dashboard'),


    


    
]

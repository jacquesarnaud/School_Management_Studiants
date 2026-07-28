from django.urls import path,include
from .views import *

urlpatterns = [
    path('users_liste',afficher_utilisateur,name='users_liste'),
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('ajouter_etudiant',ajouter_etudiant,name='ajouter_etudiant'),
    path('identifiant',identifiant,name='identifiant'),
    path('etudiant_dashboard',etu_dashboard,name='etudiant_dashboard'),
    path('mes_notes',mes_notes,name='mes_notes'),
    path('mes_absences',mes_absences,name='mes_absences'),
    path('liste_etu',list_etudiant,name='liste_etu'),

    
]

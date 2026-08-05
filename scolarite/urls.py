from django.urls import path,include
from .views import *

urlpatterns = [
    path('users_liste',afficher_utilisateur,name='users_liste'),
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('ajouter_etudiant',ajouter_etudiant,name='ajouter_etudiant'),
    path('ajouter_professeur',ajouter_professeur,name='ajouter_professeur'),
    path('identifiant',identifiant,name='identifiant'),
    path('liste_etu',list_etudiant,name='liste_etu'),
    path('liste_prof',list_professeur,name='liste_prof'),
    path('etudiant/<int:pk>/supprimer/',suprimer_etudiant,name='suprimer_etudiant'),
    path('etudiant/<int:pk>/detail/',detail_etudiant,name='detail_etudiant'),
    path('etudiant/<int:pk>/modifier/',modifier_etudiant,name='modifier_etudiant'),
    path('professeur/<int:pk>/supprimer/',suprimer_professeur,name='suprimer_professeur'),
    path('professeur/<int:pk>/detail/',detail_professeur,name='detail_professeur'),
    path('professeur/<int:pk>/modifier/',modifier_professeur,name='modifier_professeur'),



    path('etudiant_dashboard',etu_dashboard,name='etudiant_dashboard'),
    path('mes_notes',mes_notes,name='mes_notes'),
    path('mes_absences',mes_absences,name='mes_absences'),



    path('prof_dashboard',prof_dashboard,name='prof_dashboard'),
    path('ajouter-note/<int:pk>',ajouter_note,name='ajouter_note'),
    path('mes_etudiant',mes_etudiant,name='mes_etudiant'),
    path('mes_absences',mes_absences,name='mes_absences'),




]

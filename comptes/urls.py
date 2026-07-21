from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("", acceuille, name="acceuille"),
    path("deconnexion/", LogoutView.as_view(next_page="connexion"), name="logout"),

]

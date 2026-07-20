from django.urls import path
from .views import *

urlpatterns = [
    path('se-connecter/',ConnexionView.as_view(),name='vue_connexion'),
    path("home/", Home.as_view(), name="home")
]

from django.urls import path
from .views import *

urlpatterns = [
    path('',Accueille.as_view(),name='accueille' ),
    path('connexion/',Connecter.as_view(),name='connexion' )
    ]

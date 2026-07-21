from django.urls import path,include
from .views import *

urlpatterns = [
    path('login/',vue_connexion,name='login'),
    
]

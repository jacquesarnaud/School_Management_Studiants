from django.urls import path,include
from .views import *

urlpatterns = [
    path('users_liste',afficher_utilisateur,name='users_liste'),
    path('admin_dashboard',admin_dashboard,name='dashbord_admin')
    
]

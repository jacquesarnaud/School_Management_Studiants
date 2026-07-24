from django.urls import path
from django.contrib.auth.views import loginview,LogoutView

from .views import *

urlpatterns = [
    path('accueille/',Accueille.as_view(),name='accueille' )
    ]

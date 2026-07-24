from django.urls import path
from django.contrib.auth.views import loginview,LogoutView

from .views import *

urlpatterns = [
    path("login", connexionview, name="login"),
    path('logout/', LogoutView.as_view('login'), name='logout')
    ]

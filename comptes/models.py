from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):

    username = None

    email = models.EmailField(
        unique=True
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Administrateur"),
            ("professeur", "Professeur"),
            ("etudiant", "Étudiant")
        ]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):

    ROLES = [
        ('admin', 'Administrateur'),
        ('professeur', 'Professeur'),
        ('etudiant', 'Étudiant'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLES
    )

    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
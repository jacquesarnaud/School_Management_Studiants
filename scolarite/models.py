from django.db import models
from comptes.models import Utilisateur


class Classe(models.Model):
    nom_classe = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom_classe


class Matiere(models.Model):
    nom_matiere = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom_matiere


class Etudiant(models.Model):
    matricule = models.CharField(max_length=30, unique=True)
    nom       = models.CharField(max_length=100)
    prenom    = models.CharField(max_length=100)
    age       = models.IntegerField(default=0)
    classe    = models.ForeignKey(Classe,     on_delete=models.SET_NULL, null=True)
    id_user   = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,
                                     related_name='etudiant', null=True)

    def __str__(self):
        return f"{self.matricule} — {self.nom} {self.prenom}"
 

class Professeur(models.Model):
    nom       = models.CharField(max_length=100)
    prenom    = models.CharField(max_length=100)
    age       = models.IntegerField(default=0)
    matiere   = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True)
    classe    = models.ForeignKey(Classe,  on_delete=models.SET_NULL, null=True)
    id_user   = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,
                                     related_name='professeur', null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
from django.db import models
from scolarite.models import Etudiant, Matiere


class Note(models.Model):
    etudiant  = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere   = models.ForeignKey(Matiere,  on_delete=models.CASCADE)
    note      = models.FloatField()
    date     = models.DateField(auto_now_add=True)


    def __str__(self):
        return f"{self.etudiant} — {self.matiere} : {self.note}/20 ({self.date})"


class Absence(models.Model):
    STATUTS = [
        ('justifiée',     'Justifiée'),
        ('non justifiée', 'Non justifiée'),
    ]
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiere  = models.ForeignKey(Matiere,  on_delete=models.CASCADE)
    date     = models.DateField()
    status   = models.CharField(max_length=20, choices=STATUTS)

    def __str__(self):
        return f"{self.etudiant} — {self.matiere} — {self.date}"
import random
import string
from datetime import datetime
from .models import*
from comptes.models import Utilisateur


def generer_matricule(nom, prenom):

    base = f"{nom[0].upper()}{prenom[0].upper()}"
    annee     = datetime.now().year
    nombre = str(random.randint(1000, 9999))
    matricule = f"{base}--{annee}--{nombre}"

    while Etudiant.objects.filter(matricule=matricule).exists():
        matricule = f"{base}--{annee}--{nombre}"

    return f"ETU-{matricule}"


def generer_email(nom: str, prenom: str, role: str) -> str:
    nom_clean    = nom.lower().replace(" ", "")
    prenom_clean = prenom.lower().replace(" ", "")
    compteur = 1
    email = f"{prenom_clean}.{nom_clean}@{role}.school.ci"

    while Utilisateur.objects.filter(email=email).exists():
        email = f"{prenom_clean}.{nom_clean}{compteur}@{role}.school.ci"
        compteur += 1
    return email


def generer_mot_de_passe(longueur: int = 8) -> str:
    caracteres = string.ascii_letters + string.digits
    mdp  = random.choice(string.ascii_uppercase)
    mdp += random.choice(string.digits)
    mdp += ''.join(random.choices(caracteres, k=longueur - 2))
    return ''.join(random.sample(mdp, len(mdp)))
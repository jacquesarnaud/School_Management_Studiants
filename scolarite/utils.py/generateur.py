import random
import string
from datetime import datetime


def generer_matricule(nom: str, prenom: str) -> str:
    initiales = (nom[0] + prenom[0]).upper()
    annee     = datetime.now().year
    nombre    = random.randint(1000, 9999)
    return f"ETU-{initiales}-{annee}-{nombre}"


def generer_email(nom: str, prenom: str, role: str) -> str:
    nom_clean    = nom.lower().replace(" ", "")
    prenom_clean = prenom.lower().replace(" ", "")
    return f"{prenom_clean}.{nom_clean}@{role}.school.ci"


def generer_mot_de_passe(longueur: int = 8) -> str:
    caracteres = string.ascii_letters + string.digits
    mdp  = random.choice(string.ascii_uppercase)
    mdp += random.choice(string.digits)
    mdp += ''.join(random.choices(caracteres, k=longueur - 2))
    return ''.join(random.sample(mdp, len(mdp)))
# scolarite/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from scolarite.models import Etudiant, Professeur, Classe, Matiere
from notes.models import Note, Absence
from .generateur import generer_matricule, generer_email, generer_mot_de_passe
from comptes.models import Utilisateur


def vue_connexion(request):
    if request.method == 'POST':
        email    = request.POST['email']
        password = request.POST['password']
        user     = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'connexion.html', {'erreur': 'Identifiants incorrects'})
    return render(request, 'connexion.html')


@login_required
def dashboard(request):
    role = request.user.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'professeur':
        return redirect('prof_dashboard')
    elif role == 'etudiant':
        return redirect('etu_dashboard')


# ── Admin ────────────────────────────────────────────────────────────────────

def role_requis(role):
    """Décorateur personnalisé pour vérifier le rôle."""
    def decorateur(vue):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                return redirect('dashboard')
            return vue(request, *args, **kwargs)
        return wrapper
    return decorateur


@role_requis('admin')
def admin_dashboard(request):
    etudiants   = Etudiant.objects.select_related('classe').all()
    professeurs = Professeur.objects.select_related('matiere', 'classe').all()
    return render(request, 'admin/dashboard.html', {
        'etudiants':   etudiants,
        'professeurs': professeurs
    })


@role_requis('admin')
def ajouter_etudiant(request):
    if request.method == 'POST':
        nom       = request.POST['nom']
        prenom    = request.POST['prenom']
        age       = request.POST['age']
        classe_id = request.POST['classe_id']

        matricule    = generer_matricule(nom, prenom)
        email        = generer_email(nom, prenom, 'etudiant')
        mot_de_passe = generer_mot_de_passe()

        # Créer le compte utilisateur
        user = Utilisateur.objects.create_user(
            username   = email,
            email      = email,
            password   = mot_de_passe,
            first_name = nom,
            last_name  = prenom,
            role       = 'etudiant'
        )
        # Créer le profil étudiant
        Etudiant.objects.create(
            matricule = matricule,
            nom       = nom,
            prenom    = prenom,
            age       = age,
            classe_id = classe_id,
            id_user   = user
        )
        return render(request, 'admin/identifiants.html', {
            'matricule':    matricule,
            'email':        email,
            'mot_de_passe': mot_de_passe
        })

    classes = Classe.objects.all()
    return render(request, 'admin/ajouter_etudiant.html', {'classes': classes})

@role_requis('admin')
def ajouter_professeur(request):
    if request.method == 'POST':
        nom       = request.POST['nom']
        prenom    = request.POST['prenom']
        age       = request.POST['age']
        classe_id = request.POST['classe_id']
        matiere_id= request.POST['matiere_id']

        email        = generer_email(nom, prenom, 'professeur')
        mot_de_passe = generer_mot_de_passe()

        # Créer le compte utilisateur
        user = Professeur.objects.create_user(
            username   = email,
            email      = email,
            password   = mot_de_passe,
            first_name = nom,
            last_name  = prenom,
            role       = 'professeur'
        )
        # Créer le profil étudiant
        Professeur.objects.create(
            nom       = nom,
            prenom    = prenom,
            age       =age,
            matiere   = classe_id,
            classe    = matiere_id,
            id_user   = user
        )
        return render(request, 'admin/identifiants.html', {
            'email':        email,
            'mot_de_passe': mot_de_passe
        })

    classes = Classe.objects.all()
    return render(request, 'admin/ajouter_professeur.html', {'classes': classes})

# ── Professeur ───────────────────────────────────────────────────────────────

@role_requis('professeur')
def prof_dashboard(request):
    professeur = request.user.professeur
    etudiants  = Etudiant.objects.filter(classe=professeur.classe)
    return render(request, 'professeur/dashboard.html', {
        'professeur': professeur,
        'etudiants':  etudiants
    })


@role_requis('professeur')
def ajouter_note(request):
    professeur = request.user.professeur
    etudiants  = Etudiant.objects.filter(classe=professeur.classe)
    matieres   = Matiere.objects.all()

    if request.method == 'POST':
        Note.objects.update_or_create(
            etudiant_id = request.POST['etudiant_id'],
            matiere_id  = request.POST['matiere_id'],
            defaults    = {'note': request.POST['note']}
        )
        return redirect('prof_dashboard')

    return render(request, 'professeur/ajouter_note.html', {
        'etudiants': etudiants,
        'matieres':  matieres
    })


# ── Étudiant ─────────────────────────────────────────────────────────────────

@role_requis('etudiant')
def etu_dashboard(request):
    etudiant = request.user.etudiant
    notes    = Note.objects.filter(etudiant=etudiant).select_related('matiere')
    absences = Absence.objects.filter(etudiant=etudiant).select_related('matiere')

    moyenne_generale = (
        sum(n.note for n in notes) / len(notes) if notes else None
    )
    return render(request, 'etudiant/dashboard.html', {
        'etudiant':         etudiant,
        'notes':            notes,
        'absences':         absences,
        'moyenne_generale': round(moyenne_generale, 2) if moyenne_generale else None
    })
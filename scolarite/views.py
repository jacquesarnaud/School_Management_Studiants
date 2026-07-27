# scolarite/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from scolarite.models import Etudiant, Professeur, Classe, Matiere
from notes.models import Note, Absence
from .generateur import generer_matricule, generer_email, generer_mot_de_passe
from comptes.models import Utilisateur
from django.contrib import messages


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

def admin_dashboard(request):
    context = {
        "nb_utilisateurs": Utilisateur.objects.count(),
        "nb_etudiants": Etudiant.objects.count(),
        "nb_professeurs": Professeur.objects.count(),
        "nb_classes": Classe.objects.count(),
        "nb_matieres": Matiere.objects.count(),
    }

    return render(request, "scolarite/admin/accueille_admin.html", context)

def afficher_utilisateur(request):
    utilisateurs = Utilisateur.objects.all()

    return render(request, "scolarite/admin/liste_user.html", {"utilisateurs": utilisateurs})

def identifiant(request):   
    render (request,'scolarite/admin/identidiants.html',)

@role_requis('admin')
def ajouter_etudiant(request):
    classes = Classe.objects.all()

    if request.method == "POST":
        nom = request.POST["nom"]
        prenom = request.POST["prenom"]
        age = int(request.POST["age"])
        classe_id = request.POST["classe_id"]
        classe = get_object_or_404(Classe, id=classe_id)

        matricule = generer_matricule(nom, prenom)
        email = generer_email(nom, prenom, "etudiant")
        mot_de_passe = generer_mot_de_passe()

        if len(nom) >= 3 and len(prenom) >= 3 and 5 < age < 70:

            user = Utilisateur.objects.create_user(
                username=email,
                email=email,
                password=mot_de_passe,
                first_name=nom,
                last_name=prenom,
                role="etudiant",
            )

            Etudiant.objects.create(
                matricule=matricule,
                nom=nom,
                prenom=prenom,
                age=age,
                classe=classe,
                id_user=user,
            )

            messages.success(
                request,
                f"L'étudiant {nom} {prenom} a été enregistré."
            )
            return render(request, "scolarite/admin/identifiants.html", {
                                "nom": nom,
                                "prenom": prenom,
                                "email": email,
                                "mot_de_passe": mot_de_passe,
                                "matricule": matricule,
                                "role": "etudiant",
                            })

        messages.error(
            request,
            "Le nom et le prénom doivent contenir au moins 3 caractères et l'âge doit être compris entre 6 et 69 ans."
        )

    return render(
        request,
        "scolarite/admin/ajouter_etudiant.html",
        {"classes": classes},
    )
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
        if len(nom) == 3 and len(prenom) == 3 and 5 < age < 70:
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
            redirect(request, 'scolarite/admin/identifiants.html', {
                'email':        email,
                'mot_de_passe': mot_de_passe
            })

    classes = Classe.objects.all()
    return render(request, 'scolarite/admin/ajouter_prof.html', {'classes': classes})

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

def etudiant_dashboard(request):
    context = {
        "classes": Classe.objects.filter(Classe=Classe),
        "matieres": Matiere.objects.all(),
    }
    return render (request,'comptes/etudiant/accueille_etudiant.html', context)
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
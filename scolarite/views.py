# scolarite/views.py
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from scolarite.models import Etudiant, Professeur, Classe, Matiere
from notes.models import Note, Absence
from .generateur import generer_matricule, generer_email, generer_mot_de_passe
from comptes.models import Utilisateur
from django.contrib import messages
from functools import wraps
from django.core.exceptions import PermissionDenied
from .forms import *
from django.db import transaction
from .forms import*
from django.db.models import Avg

# ── Admin ────────────────────────────────────────────────────────────────────

def role_requis(role):
    def decorateur(vue):
        @wraps(vue)
        @login_required
        def wrapper(request, *args, **kwargs):
            if getattr(request.user, "role", None) != role:
                raise PermissionDenied("Vous n'avez pas l'autorisation d'accéder à cette page.")
            return vue(request, *args, **kwargs)
        return wrapper
    return decorateur

@role_requis('admin')
def admin_dashboard(request):
    context = {
        "nb_utilisateurs": Utilisateur.objects.count(),
        "nb_etudiants": Etudiant.objects.count(),
        "nb_professeurs": Professeur.objects.count(),
        "nb_classes": Classe.objects.count(),
        "nb_matieres": Matiere.objects.count(),
    }
    return render(request, "scolarite/admin/accueille_admin.html", context)

@role_requis('admin')
def afficher_utilisateur(request):
    utilisateurs = Utilisateur.objects.all()
    return render(request, "scolarite/admin/liste_user.html", {"utilisateurs": utilisateurs})

@role_requis('admin')
def identifiant(request):   
    render (request,'scolarite/admin/identidiants.html',)

@role_requis('admin')
def list_etudiant(request):
    etudiants = Etudiant.objects.all()

    context = {
        "etudiants": etudiants
    }

    return render(request, "scolarite/admin/liste_etud_registe.html", context)

@role_requis('admin')
def ajouter_etudiant(request):

    if request.method == "POST":
        form = Etudiantforms(request.POST)
        if form.is_valid():

            nom = form.cleaned_data["nom"]
            prenom = form.cleaned_data["prenom"]
            age = int(form.cleaned_data["age"])
            classe_id = form.cleaned_data["classe"]

            matricule = generer_matricule(nom, prenom)
            email = generer_email(nom, prenom, "etudiant")
            mot_de_passe = generer_mot_de_passe()

        
            try:

                with transaction.atomic():

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
                        classe=classe_id,
                        id_user=user,
                    )

                messages.success(
                    request,
                    f"L'étudiant {nom} {prenom} a été enregistré."
                )

                return render(
                    request,
                    "scolarite/admin/identifiants.html",
                    {
                        "nom": nom,
                        "prenom": prenom,
                        "email": email,
                        "mot_de_passe": mot_de_passe,
                        "matricule": matricule,
                        "role": "etudiant",
                    }
                )
            except Exception as e:

                messages.error(
                    request,
                    "Une erreur est survenue pendant l'enregistrement."
                )

    else:
        form = Etudiantforms()


    return render(
        request,
        "scolarite/admin/ajouter_etudiant.html",
        {"form": form},
    )

@role_requis('admin')
def suprimer_etudiant(request , pk):
    etudiant = get_object_or_404(Etudiant,pk=pk)
    if request.method == 'POST':
        etudiant.id_user.delete()
        return redirect('liste_etu')
 
    return render(request, "scolarite/admin/supprimer.html", {
        "etudiant": etudiant
    })

@role_requis('admin')
def detail_etudiant(request , pk):
    etudiant = get_object_or_404(Etudiant,pk=pk)
    return render(request, "scolarite/admin/detail.html", {
            "etudiant": etudiant
        })

def modifier_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)

    if request.method == "POST":
        form = Etudiantforms(request.POST, instance=etudiant)

        if form.is_valid():
            form.save()
            return redirect("liste_etu")
            messages.success(request,'modification effectuer')
    else:
        form = Etudiantforms(instance=etudiant)
        messages.error(request,'error modification pas pris en compte')

    return render(request, "scolarite/admin/update.html", {
        "form": form
    })

@role_requis('admin')
def ajouter_professeur(request):
    form = Professeurforms() 
    if request.method == 'POST':
        form = Professeurforms(request.POST)
        if form.is_valid():

            nom       = form.cleaned_data['nom']
            prenom    = form.cleaned_data['prenom']
            age       = int(form.cleaned_data['age']) 
            classe    = form.cleaned_data['classe']
            matiere   = form.cleaned_data['matiere']

            

            email        = generer_email(nom, prenom, 'professeur')
            mot_de_passe = generer_mot_de_passe()
            
            try:
                with transaction.atomic():
                    user = Utilisateur.objects.create_user(
                        username   = email,
                        email      = email,
                        password   = mot_de_passe,
                        first_name = nom,
                        last_name  = prenom,
                        role       = 'professeur'
                    )
                    Professeur.objects.create(
                        nom       = nom,
                        prenom    = prenom,
                        age       = age,
                        matiere   = matiere,
                        classe    = classe,
                        id_user   = user
                    )
                    messages.success(
                    request,
                    f"le Professeur {nom} {prenom} a été enregistré."
                    )
                    return render(request, 'scolarite/admin/identifiants.html', {
                        'email':        email,
                        'mot_de_passe': mot_de_passe
                    })
            except Exception:   
                messages.error(request,"Une erreur est survenue pendant l'enregistrement.")
    else:
        form = Professeurforms() 

    return render(request, 'scolarite/admin/ajouter_prof.html', { 'form' : form })

@role_requis('admin')
def suprimer_professeur(request , pk):
    professeur = get_object_or_404(Professeur,pk=pk)
    if request.method == 'POST':
        professeur.id_user.delete()
        return redirect('liste_prof')

    return render(request, "scolarite/admin/supprimer_prof.html", {
        "professeur": professeur
    })

@role_requis('admin')
def detail_professeur(request , pk):
    professeur = get_object_or_404(Professeur,pk=pk)
    return render(request, "scolarite/admin/detail_prof.html", {
            "professeur": professeur
        })

@role_requis('admin')
def list_professeur(request):
    professeurs = Professeur.objects.all()

    context = {
        "professeurs": professeurs
    }

    return render(request, "scolarite/admin/liste_prof_registe.html", context)

def modifier_professeur(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)

    if request.method == "POST":
        form = Professeurforms(request.POST, instance=professeur)

        if form.is_valid():
            form.save()
            messages.success(request,'modification effectuer')
            return redirect("liste_prof")
        messages.error(request,'error modification pas pris en compte')

    form = Professeurforms(instance=professeur)

    return render(request, "scolarite/admin/update_prof.html", {
        "form": form
    })

# ── Professeur ───────────────────────────────────────────────────────────────

def prof_dashboard(request):
    professeur = Professeur.objects.all()
    return render(request, 'scolarite/professeur/accueille_professeur.html', {
        'professeur': professeur,
    })


@role_requis('professeur')
def ajouter_note(request,pk):
    professeur = request.user.professeur
    etudiant = get_object_or_404( Etudiant,pk=pk)  
    matieres = professeur.matiere

    if request.method == 'POST':
        Note.objects.create(
            etudiant = etudiant,
            matiere=matieres,
            note=request.POST['note']  )      
        return redirect('prof_dashboard')

    return render(request, 'scolarite/professeur/ajouter_note.html', {
        'etudiant': etudiant,
        'matieres':  matieres
    })

def mes_etudiant(request):
    professeur = request.user.professeur
    etudiants = Etudiant.objects.filter(classe = professeur.classe)  
    if etudiants:
        for etu in etudiants:
            etu.notes = Note.objects.filter(
            etudiant=etu.id).select_related('matiere')

            etu.moyenne = Note.objects.filter(
                etudiant=etu
            ).aggregate(
                moyenne=Avg('note')
            )['moyenne']    
    return render(request,'scolarite/professeur/mes_etudiant.html', {'etudiants':etudiants})

# ── Étudiant ─────────────────────────────────────────────────────────────────
@role_requis('etudiant')
def etu_dashboard(request):

    etudiant = request.user.etudiant

    classe = etudiant.classe

    matieres = Matiere.objects.filter(
        professeur__classe=classe
    ).distinct()

    context = {
        "etudiant": etudiant,
        "classe": classe,
        "matieres": matieres,
    }

    return render(
        request,
        "scolarite/etudiants/accueille_etudiant.html",
        context
    )

@role_requis('etudiant')
def mes_notes(request):

    etudiant = request.user.etudiant

    notes = Note.objects.filter(
        etudiant=etudiant
    ).select_related('matiere')


    return render(
        request,
        'scolarite/etudiants/notes.html',
        {
            'etudiant': etudiant,
            'notes': notes,
        }
    )
@role_requis('etudiant')
def mes_absences(request):

    etudiant = request.user.etudiant


    absences = Absence.objects.filter(
        etudiant=etudiant
    ).select_related('matiere')


    return render(
        request,
        'scolarite/etudiants/absences.html',
        {
            'etudiant': etudiant,
            'absences': absences,
        }
    )
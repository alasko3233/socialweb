from django.shortcuts import redirect, render
from account.models import FollowerCount, Post, Profile
from django.contrib.auth.models import User
from django.contrib import messages
import pdb
from django.contrib.auth.decorators import login_required

from chat.models import Thread

# Create your views here.


@login_required
def account_setting_edit(request):
    # Fonction pour éditer les paramètres du compte utilisateur

    # Récupération de l'utilisateur actuel
    identique = request.user

    # Récupération des paramètres utilisateur à partir du modèle Profile
    user_setting = Profile.objects.get(user=request.user)
    user = request.user

    # Calcul du nombre de followers et followings de l'utilisateur
    user_followers = len(FollowerCount.objects.filter(follower=user.username))
    user_followings = len(
        FollowerCount.objects.filter(user_name=user.username))

    # Création du contexte avec les données à transmettre au template
    context = {
        "profile": user_setting,
        'identique': identique,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }

    if request.method == 'POST':
        # Vérification si la requête est de type POST

        if request.FILES.get('photo') == None:
            # Vérification si aucune photo n'est téléchargée

            # Mise à jour des informations utilisateur à partir des données POST
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            about = request.POST['about']
            ville = request.POST['ville']
            pays = request.POST['pays']
            telephone = request.POST['telephone']
            genre = request.POST['genre']
            birtdhay = request.POST['birtdhay']

            if birtdhay:
                # Vérification si la date de naissance est spécifiée
                user_setting.date_of_birth = birtdhay
            else:
                pass

            # Récupération de la photo existante
            photos = user_setting.photo

            # Mise à jour des informations utilisateur dans le modèle Profile
            user_setting.bio = about
            user_setting.genre = genre
            user_setting.telephone = telephone
            user_setting.pays = pays
            user_setting.ville = ville
            user_setting.photo = photos

            # Sauvegarde des modifications dans les modèles User et Profile
            user.save()
            user_setting.save()

        if request.FILES.get('photo') != None:
            # Vérification si une nouvelle photo est téléchargée

            # Mise à jour des informations utilisateur à partir des données POST
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            about = request.POST['about']
            ville = request.POST['ville']
            pays = request.POST['pays']
            telephone = request.POST['telephone']
            genre = request.POST['genre']
            birtdhay = request.POST['birtdhay']

            # Récupération de la nouvelle photo
            photos = request.FILES.get('photo')

            if birtdhay:
                # Vérification si la date de naissance est spécifiée
                user_setting.date_of_birth = birtdhay
            else:
                pass

            # Mise à jour des informations utilisateur dans le modèle Profile
            user_setting.bio = about
            user_setting.genre = genre
            user_setting.telephone = telephone
            user_setting.pays = pays
            user_setting.ville = ville
            user_setting.photo = photos

            # Sauvegarde des modifications dans les modèles User et Profile
            user.save()
            user_setting.save()

        # Redirection vers la page d'accueil des paramètres du compte avec un message
        messages.info(request, 'Profil modifié')
        return redirect('setting_accueil', user.username)

    # Rendu du template pour l'édition des paramètres du compte
    return render(request, 'settings/account_setting_edit.html', context)


@login_required
def setting_accueil(request, pk):
    # Fonction pour afficher la page d'accueil des paramètres avec les publications de l'utilisateur

    # Récupération des utilisateurs suivis par l'utilisateur actuel
    user_follings = FollowerCount.objects.filter(user_name=pk)

    # Récupération des amis de l'utilisateur actuel (même que user_follings)
    friends = FollowerCount.objects.filter(user_name=pk)

    # Récupération de l'objet utilisateur et du profil utilisateur correspondant à l'identifiant 'pk'
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)

    # Récupération des publications de l'utilisateur actuel
    posts_user = Post.objects.filter(user=user_object)

    pk = pk
    follower = request.user.username

    # Vérification si l'utilisateur actuel suit l'utilisateur de la page d'accueil
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    # Vérification si l'utilisateur actuel est le même que l'utilisateur de la page d'accueil
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Calcul du nombre de followers et followings de l'utilisateur de la page d'accueil
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
        'user_follings': user_follings
    }

    user = request.user

    # Rendu du template pour la page d'accueil des paramètres
    return render(request, 'settings/pages/accueil.html', context)


@login_required
def post(request):
    # Fonction pour créer et publier un nouveau post

    user = request.user
    caption = request.POST['caption']
    images = request.FILES.get('image')

    # Création d'une nouvelle instance du modèle Post avec les données fournies
    new_post = Post.objects.create(
        user=user, image=images, caption=caption, user_name=user.username)

    # Sauvegarde du nouveau post
    new_post.save()

    # Affichage d'un message d'information
    messages.info(request, 'Post publié')

    # Redirection vers la page d'accueil
    return redirect('accueil')


@login_required
def cover(request):
    # Fonction pour mettre à jour la couverture du profil utilisateur

    user = request.user
    user_setting = Profile.objects.get(user=request.user)
    cover = request.FILES.get('cover')

    # Mise à jour de la couverture dans le modèle Profile
    user_setting.cover = cover

    # Sauvegarde des modifications dans les modèles User et Profile
    user.save()
    user_setting.save()

    # Affichage d'un message d'information
    messages.info(request, 'couverture changer')

    # Redirection vers la page précédente
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def renitialiser(request):
    # Fonction pour réinitialiser la couverture du profil utilisateur

    user = request.user
    user_setting = Profile.objects.get(user=request.user)

    # Suppression de la couverture en définissant sa valeur à None
    user_setting.cover = None

    # Sauvegarde des modifications dans le modèle Profile
    user_setting.save()

    # Affichage d'un message d'information
    messages.info(request, 'couverture changer')

    # Redirection vers la page précédente
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def send_message(request, pk):
    # Fonction pour envoyer un message à un utilisateur spécifié

    user = request.user
    user_object = User.objects.get(username=pk)

    # Vérification de l'existence d'une conversation entre les deux utilisateurs
    if Thread.objects.filter(first_person=user, second_person=user_object).first():
        return redirect('chat')
    elif Thread.objects.filter(first_person=user_object, second_person=user).first():
        return redirect('chat')
    else:
        # Création d'une nouvelle conversation entre les deux utilisateurs
        new_thread = Thread.objects.create(
            first_person=user, second_person=user_object)
        new_thread.save()
        return redirect('chat')

    # Redirection vers la page de chat
    return redirect('chat')


@login_required
def profile(request, pk):
    # Fonction pour afficher le profil utilisateur

    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)

    # Vérification si l'utilisateur actuel est le même que l'utilisateur du profil
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
    }

    # Rendu du template pour la page de profil
    return render(request, 'settings/pages/profile/accueil.html', context)


@login_required
def setting_galerie(request, pk):
    # Fonction pour afficher la galerie de l'utilisateur

    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username

    # Vérification si l'utilisateur actuel suit l'utilisateur de la galerie
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    # Vérification si l'utilisateur actuel est le même que l'utilisateur de la galerie
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Calcul du nombre de followers et followings de l'utilisateur de la galerie
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }

    # Rendu du template pour la page de galerie
    return render(request, 'settings/pages/galerie.html', context)


@login_required
def setting_amis(request, pk):
    # Fonction pour afficher la liste d'amis de l'utilisateur

    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username

    # Vérification si l'utilisateur actuel suit l'utilisateur de la liste d'amis
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    # Vérification si l'utilisateur actuel est le même que l'utilisateur de la liste d'amis
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Calcul du nombre de followers et followings de l'utilisateur de la liste d'amis
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    # Récupération des followers et followings de l'utilisateur de la liste d'amis
    followers = FollowerCount.objects.filter(follower=pk)
    followings = FollowerCount.objects.filter(user_name=pk)

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
        'followings': followings,
        'followers': followers,
    }

    # Rendu du template pour la page d'amis
    return render(request, 'settings/pages/amis.html', context)


@login_required
def setting_about(request, pk):
    # Fonction pour afficher les informations sur l'utilisateur

    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username

    # Vérification si l'utilisateur actuel suit l'utilisateur des informations
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    # Vérification si l'utilisateur actuel est le même que l'utilisateur des informations
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Calcul du nombre de followers et followings de l'utilisateur des informations
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }

    # Rendu du template pour la page des informations
    return render(request, 'settings/pages/about.html', context)


def edit_password(request):
    # Fonction pour afficher les informations sur l'utilisateur
    user = request.user

    user_object = User.objects.get(username=user.username)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)

    follower = request.user.username

    # Vérification si l'utilisateur actuel suit l'utilisateur des informations
    if FollowerCount.objects.filter(user_name=user.username, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    # Vérification si l'utilisateur actuel est le même que l'utilisateur des informations
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    # Calcul du nombre de followers et followings de l'utilisateur des informations
    user_followers = len(FollowerCount.objects.filter(follower=user.username))
    user_followings = len(
        FollowerCount.objects.filter(user_name=user.username))

    # Création du contexte avec les données à transmettre au template
    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }

    # Rendu du template pour la page des informations
    return render(request, 'settings/pages/edit_password.html', context)


def update_password(request):
    user = request.user
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')
        old_password = request.POST.get('old_password')

        # Vérifier si les mots de passe entrés correspondent
        if new_password == new_password2:
            # Vérifier si le mot de passe actuel est correct
            if request.user.check_password(old_password):
                # Mettre à jour le mot de passe de l'utilisateur
                request.user.set_password(new_password)
                request.user.save()
                # Rediriger vers une page de succès ou afficher un message de succès

                # Exemple de redirection vers la page d'accueil
                messages.success(request, "Mot de passe changé avec success")

                return redirect('setting_accueil', user.username)
            else:
                # Le mot de passe actuel est incorrect, afficher un message d'erreur
                messages.error(
                    request, "L'ancien mot de passe n'est pas correct.")
                return redirect('edit_password')

        else:
            # Les mots de passe entrés ne correspondent pas, afficher un message d'erreur
            messages.error(
                request, "Les nouveaux mots de passe de sont pas identiques.")
            return redirect('edit_password')

    # Si la méthode de requête n'est pas POST ou si une erreur s'est produite, rediriger vers la page du formulaire
    return redirect('setting_accueil', user.username)

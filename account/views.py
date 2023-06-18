from itertools import chain
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import LoginForm, UserRegistrationForm, \
    UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Activity, Comment, FollowerCount, LikePost, Post, Profile
from django.contrib import messages
from django.contrib.auth.models import User


def loginn(request):
    if request.method == 'POST':
        # Récupération du nom d'utilisateur et du mot de passe depuis la requête POST
        username = request.POST['username']
        password = request.POST['password']

        # Authentification de l'utilisateur
        user = authenticate(username=username, password=password)

        # Vérification si l'utilisateur existe
        if user is not None:
            # Vérification si le compte de l'utilisateur est actif
            if user.is_active:
                # Connexion de l'utilisateur
                login(request, user)
                return redirect('accueil')
            else:
                # Le compte de l'utilisateur est désactivé
                messages.info(request, 'Votre compte est désactivé')
                return redirect('login')
        else:
            # Nom d'utilisateur ou mot de passe incorrect
            messages.info(request, 'Email ou mot de passe incorrect')
            return redirect('login')
    else:
        # Affichage de la page de connexion
        return render(request, 'account/login1.html')


def registers(request):
    if request.method == 'POST':
        # Récupération du nom d'utilisateur, de l'e-mail et des mots de passe depuis la requête POST
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Vérification si les deux mots de passe sont identiques
        if password == password2:
            # Vérification si l'e-mail existe déjà
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Cet email est déjà utilisé')
                return redirect('register')
            # Vérification si le nom d'utilisateur existe déjà
            elif User.objects.filter(username=username).exists():
                messages.info(
                    request, 'Cet nom d\'utilisateur est déjà utilisé')
                return redirect('register')
            else:
                # Création de l'utilisateur
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()

                # Création du profil de l'utilisateur
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(
                    user=user_model, id_user=user_model.id)
                new_profile.save()

                return redirect('login')
        else:
            # Les mots de passe ne sont pas identiques
            messages.info(request, 'Les mots de passe ne sont pas identiques')
            return redirect('register')

    # Affichage de la page d'inscription
    return render(request, 'account/register1.html')


def logout_user(request):
    # Déconnexion de l'utilisateur
    logout(request)
    return redirect('login')


@login_required
def upload(request):
    # Affichage de la page de téléchargement (accessible uniquement aux utilisateurs connectés)
    return render(request, 'account/register1.html')


@login_required
def accueil(request):
    user = request.user

    user_follows_list = []
    feed = []

    # Récupération de la liste des utilisateurs suivis par l'utilisateur actuel
    user_follings = FollowerCount.objects.filter(
        user_name=request.user.username)

    # Récupération de la liste des utilisateurs qui suivent l'utilisateur actuel
    user_folling = FollowerCount.objects.filter(follower=request.user.username)

    # Construction du fil d'actualité en récupérant les publications des utilisateurs suivis
    for user in user_folling:
        user_follows_list.append(user.user_name)

    for usernames in user_follows_list:
        feed_list = Post.objects.filter(user_name=usernames)
        feed.append(feed_list)

    # Concaténation de toutes les publications pour afficher dans le fil d'actualité
    feed_lists = list(chain(*feed))

    # Préparation du contexte pour le rendu de la page
    context = {
        'posts': feed_lists,
        'user_follings': user_follings
    }

    return render(request, 'account/dashboard.html', context)


@login_required
def like_post(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)

    # Vérification si l'utilisateur a déjà aimé la publication
    like_filter = LikePost.objects.filter(post_id=post.id, user=user).first()

    if like_filter == None:
        # L'utilisateur n'a pas encore aimé la publication
        new_like = LikePost.objects.create(
            post_id=post.id, user=user, user_name=user.username)
        new_like.save()

        # Mise à jour du nombre de likes de la publication
        post.no_of_likes = post.no_of_likes+1
        post.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        # L'utilisateur a déjà aimé la publication, donc on supprime le like
        like_filter.delete()

        # Mise à jour du nombre de likes de la publication
        post.no_of_likes = post.no_of_likes-1
        post.save()

        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        userfollow = request.POST['userfollow']

        # Vérification si l'utilisateur actuel suit déjà l'utilisateur donné
        if FollowerCount.objects.filter(follower=follower, user_name=userfollow).first():
            # L'utilisateur actuel suit déjà l'utilisateur donné, donc on supprime le suivi
            delete_follower = FollowerCount.objects.get(
                follower=follower, user_name=userfollow)
            delete_follower.delete()
            return redirect('setting_accueil', userfollow)
        else:
            # L'utilisateur actuel ne suit pas encore l'utilisateur donné, donc on ajoute le suivi
            new_follower = FollowerCount.objects.create(
                follower=follower, user_name=userfollow, user=request.user)
            new_follower.save()
            return redirect('setting_accueil', userfollow)
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def comment(request):
    user = request.user
    comment = request.POST['comment']

    if comment:
        post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)

        # Création du commentaire pour la publication donnée
        new_comment = Comment.objects.create(
            user=user, post=post, body=comment)
        new_comment.save()

        user_of_post = User.objects.get(username=post.user)
        type_of_activity = "Commenter"

        # Création de l'activité associée au commentaire
        new_activity = Activity.objects.create(
            user=user_of_post, activity_type=type_of_activity, related_post=post, other_username=user.username)
        new_activity.save()
    else:
        pass

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request):
    if request.method == 'POST':
        # Récupération des données de modification de l'utilisateur depuis la requête POST
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES)

        # Vérification si les formulaires de modification sont valides
        if user_form.is_valid() and profile_form.is_valid():
            # Sauvegarde des modifications de l'utilisateur et de son profil
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profil mis à jour avec succès')
        else:
            messages.error(
                request, 'Erreur lors de la mise à jour de votre profil')
    else:
        # Affichage des formulaires de modification de l'utilisateur et de son profil
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def search_users(request):
    query = request.GET.get('query', '').strip()

    if not query:
        return JsonResponse({'message': 'Aucune donnée disponible'})

    # Recherche des utilisateurs dont le nom d'utilisateur contient la requête de recherche
    users = User.objects.filter(username__icontains=query).values('username')

    return JsonResponse(list(users), safe=False)

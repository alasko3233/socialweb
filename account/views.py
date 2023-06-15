from itertools import chain
from django.http import HttpResponse
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('accueil')
            else:
                messages.info(request, 'votre compte est desactiver')
                return redirect('login')
        else:
            messages.info(request, 'email ou mot de passe incorrect')
            return redirect('login')
    else:
        return render(request, 'account/login1.html')


def registers(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # verifier si les 2 mots de passe sont identique
        if password == password2:
            # verifier si l email existe deja
            if User.objects.filter(email=email).exists():
                messages.info(request, 'cet email est deja utilisé')
                return redirect('register')
        # verifier si cet username existe deja
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'cet username est deja utilisé')
                return redirect('register')
            else:
                # Creation de l'utilisateur
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
            # Creation de son profile
            user_model = User.objects.get(username=username)
            new_profile = Profile.objects.create(
                user=user_model, id_user=user_model.id)
            new_profile.save()
            return redirect('login')
            # new_user = user_form.save(commit=False)
            pass
        else:
            messages.info(request, 'Les mots de passe sont pas identique')
            return redirect('register')

    return render(request, 'account/register1.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def upload(request):
    return render(request, 'account/register1.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authentification réussie')
                else:
                    return HttpResponse('Compte désactivé')
            else:
                return HttpResponse('Identifiants de connexion invalides')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
         # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
 # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
 # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'account/dashboard.html', context)


@login_required
def accueil(request):
    user = request.user

    user_follows_list = []
    feed = []
    user_follings = FollowerCount.objects.filter(
        user_name=request.user.username)

    user_folling = FollowerCount.objects.filter(follower=request.user.username)

    for user in user_folling:
        user_follows_list.append(user.user_name)

    for usernames in user_follows_list:
        feed_list = Post.objects.filter(user_name=usernames)
        feed.append(feed_list)
    feed_lists = list(chain(*feed))
    # posts = Post.objects.all()
    print(user_login)
    context = {
        'posts': feed_lists,
        'user_follings': user_follings
    }

    return render(request, 'account/dashboard.html', context)


@login_required
def like_post(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post.id, user=user).first()

    if like_filter == None:
        new_like = LikePost.objects.create(
            post_id=post.id, user=user, user_name=user.username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        userfollow = request.POST['userfollow']
        if FollowerCount.objects.filter(follower=follower, user_name=userfollow).first():
            delete_follower = FollowerCount.objects.get(
                follower=follower, user_name=userfollow)
            delete_follower.delete()
            return redirect('setting_accueil', userfollow)
        else:
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
    post_id = request.POST['post_id']
    post = Post.objects.get(id=post_id)
    new_comment = Comment.objects.create(
        user=user, post=post, body=comment)
    new_comment.save()
    user_of_post = User.objects.get(username=post.user)
    type_of_activity = "Commenter"
    new_activity = Activity.objects.create(
        user=user_of_post, activity_type=type_of_activity, related_post=post, other_username=user.username)
    new_activity.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated '
                             'successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

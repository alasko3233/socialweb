from django.shortcuts import redirect, render
from account.models import FollowerCount, Post, Profile
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.


def account_setting_edit(request):
    identique = request.user
    user_setting = Profile.objects.get(user=request.user)
    user = request.user
    user_followers = len(FollowerCount.objects.filter(follower=user.username))
    user_followings = len(
        FollowerCount.objects.filter(user_name=user.username))

    context = {"profile": user_setting,
               'identique': identique,
               'user_followers': user_followers,
               'user_followings': user_followings,

               }
    if request.method == 'POST':
        if request.FILES.get('photo') == None:
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            about = request.POST['about']
            ville = request.POST['ville']
            pays = request.POST['pays']
            telephone = request.POST['telephone']
            genre = request.POST['genre']
            birtdhay = request.POST['birtdhay']
            photos = user_setting.photo
            user_setting.bio = about
            user_setting.date_of_birth = birtdhay
            user_setting.genre = genre
            user_setting.telephone = telephone
            user_setting.pays = pays
            user_setting.ville = ville
            user_setting.photo = photos
            user.save()
            user_setting.save()
        if request.FILES.get('photo') != None:
            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            about = request.POST['about']
            ville = request.POST['ville']
            pays = request.POST['pays']
            telephone = request.POST['telephone']
            genre = request.POST['genre']
            birtdhay = request.POST['birtdhay']
            photos = request.FILES.get('photo')
            user_setting.bio = about
            user_setting.date_of_birth = birtdhay
            user_setting.genre = genre
            user_setting.telephone = telephone
            user_setting.pays = pays
            user_setting.ville = ville
            user_setting.photo = photos
            user.save()
            user_setting.save()
        user = request.user
        messages.info(request, 'Profil modifié')
        return redirect('setting_accueil', user.username)
    return render(request, 'settings/account_setting_edit.html', context)


def setting_accueil(request, pk):
    user_follings = FollowerCount.objects.filter(
        user_name=pk)
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'
    if user_object == request.user:
        identique = user_object
    else:
        identique = None
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))
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
    return render(request, 'settings/pages/accueil.html', context)


def post(request):
    user = request.user
    caption = request.POST['caption']
    images = request.FILES.get('image')
    new_post = Post.objects.create(
        user=user, image=images, caption=caption, user_name=user.username)
    new_post.save()
    messages.info(request, 'Post publié')
    return redirect('accueil')


def profile(request, pk):
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    if user_object == request.user:
        identique = user_object
    else:
        identique = None

    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,

    }
    return render(request, 'settings/pages/profile/accueil.html', context)


def setting_galerie(request, pk):
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    if user_object == request.user:
        identique = user_object
    else:
        identique = None
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,


    }
    return render(request, 'settings/pages/galerie.html', context)


def setting_amis(request, pk):
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    if user_object == request.user:
        identique = user_object
    else:
        identique = None
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))
    followers = FollowerCount.objects.filter(follower=pk)
    followings = FollowerCount.objects.filter(user_name=pk)

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
    return render(request, 'settings/pages/amis.html', context)


def setting_about(request, pk):
    user_object = User.objects.get(username=pk)
    profil_of_user = Profile.objects.get(user=user_object)
    posts_user = Post.objects.filter(user=user_object)
    pk = pk
    follower = request.user.username
    if FollowerCount.objects.filter(user_name=pk, follower=follower).first():
        btn = 'Unfollow'
    else:
        btn = 'Follow'

    if user_object == request.user:
        identique = user_object
    else:
        identique = None
    user_followers = len(FollowerCount.objects.filter(follower=pk))
    user_followings = len(FollowerCount.objects.filter(user_name=pk))

    context = {
        'userS': user_object,
        'posts': posts_user,
        'profil_of_user': profil_of_user,
        'identique': identique,
        'btn': btn,
        'user_followers': user_followers,
        'user_followings': user_followings,
    }
    return render(request, 'settings/pages/about.html', context)

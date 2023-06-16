from django.db import models
from django.conf import settings
import uuid
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_user = models.IntegerField(null=True)
    date_of_birth = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='users/profile/%Y/%m/',
                              blank=True, null=True)
    cover = models.ImageField(upload_to='users/cover/%Y/%m/',
                              blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover:
            img = Image.open(self.cover.path)
            img = img.resize((1366, 400))
            img.save(self.cover.path)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='post_image/%Y/%m/',
                              blank=True, null=True)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

    def get_comments(self):
        comments = Comment.objects.filter(post=self)
        return comments

    def get_comment_count(self):
        comment_count = Comment.objects.filter(post=self).count()
        return comment_count


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user


class FollowerCount(models.Model):
    follower = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user

    def get_user_profile(self):
        user = User.objects.get(username=self.follower)
        return user.profile

    def get_user_profile_image_url(self):
        profile = self.get_user_profile()
        if profile and profile.photo:
            return profile.photo.url
        return None


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    def get_username(self):
        return self.user.username

    def get_user_profile(self):
        return self.user.profile

    def get_user_profile_image_url(self):
        profile = self.get_user_profile()
        if profile and profile.photo:
            return profile.photo.url
        return None


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    other_username = models.CharField(max_length=100, blank=True, null=True)
    activity_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    content = models.TextField(blank=True)
    related_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    is_viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    def other_user_profile(self):
        user = User.objects.get(username=self.other_username)
        profile = Profile.objects.get(user=user)
        return profile

    def other_user_profile_image_url(self):
        profile = self.other_user_profile()
        if profile and profile.photo:
            return profile.photo.url
        return None

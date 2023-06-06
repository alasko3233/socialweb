from django.db import models
from django.conf import settings
import uuid
from datetime import datetime
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    id_user = models.IntegerField(null=True)
    date_of_birth = models.DateField(blank=True, null=True)
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

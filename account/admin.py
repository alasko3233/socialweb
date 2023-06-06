from django.contrib import admin

from account.models import LikePost, Post, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)

from django.urls import path, include
from . import views
urlpatterns = [
    path('edit/', views.account_setting_edit,
         name='account_setting_edit'),
    path('accueil/<str:pk>', views.setting_accueil, name='setting_accueil'),
    path('galerie/<str:pk>', views.setting_galerie, name='setting_galerie'),
    path('about/<str:pk>', views.setting_about, name='setting_about'),
    path('amis/<str:pk>', views.setting_amis, name='setting_amis'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('post/', views.post, name='post'),
    path('cover/', views.cover, name='cover'),
    path('renitialiser/', views.renitialiser, name='renitialiser'),
    path('send_message/<str:pk>', views.send_message, name='send_message'),


    path('edit_password/', views.edit_password,
         name='edit_password'),
    path('update_password/', views.update_password,
         name='update_password'),

]

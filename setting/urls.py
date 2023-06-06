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



]

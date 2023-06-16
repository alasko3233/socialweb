from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', views.loginn, name='login'),

    # login / logout urls
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # # change password urls
    # path('password-change/', auth_views.PasswordChangeView.as_view(),
    #      name='password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
    #      name='password_change_done'),
    # # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="reset/reset_password.html"),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reset/password_reset_sent.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="reset/password_reset_form.html"), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset/password_reset_done.html"),
         name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),
    path('', views.accueil, name='dashboard'),
    path('register/', views.registers, name='register'),
    path('accueil/', views.accueil, name='accueil'),
    path('upload/', views.upload, name='upload'),

    path('like_post?post_id<str:post_id>', views.like_post, name='like_post'),
    path('follow/', views.follow, name='follow'),
    path('comment/', views.comment, name='comment'),



    path('account/search-users/', views.search_users, name='search_users'),
    path('logout_user/', views.logout_user, name='logout_user'),



    path('edit/', views.edit, name='edit'),
    # path('login/', views.user_login, name='login'),
]

from account.models import Profile


def profile_context(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            pass
    # Récupérer les informations de profil
    # Supposons que vous ayez un modèle de profil nommé 'Profile'
    # Renvoyer le dictionnaire de contexte
    return {'user_profile': profile}

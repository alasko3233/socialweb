from account.models import Activity, Profile


def profile_context(request):
    profile = None
    activities = None
    total_activities = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            activities = Activity.objects.filter(user=request.user)
            total_activities = activities.count()
        except Profile.DoesNotExist:
            pass
    # Récupérer les informations de profil
    # Supposons que vous ayez un modèle de profil nommé 'Profile'
    # Renvoyer le dictionnaire de contexte
    return {
        'user_profile': profile,
        'user_activities': activities,
        'total_activities': total_activities
    }

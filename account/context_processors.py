from account.models import Activity, Profile
from chat.models import Thread


def profile_context(request):
    profile = None
    activities = None
    total_activities = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            activities = Activity.objects.filter(user=request.user)
            total_activities = activities.count()
            threads = Thread.objects.by_user(user=request.user)
            thread_data = []
            no_discussion = threads.count()
            for thread in threads:
                # Récupérer l'autre utilisateur du thread
                other_user = thread.get_other_user(request.user)
                # Récupérer le dernier message de l'autre utilisateur
                last_message = thread.get_last_message_by_other_user(
                    request.user)
                thread_data.append({
                    'thread': thread,
                    'other_user': other_user,
                    'last_message': last_message,
                })

        except Profile.DoesNotExist:
            pass
    # Récupérer les informations de profil
    # Supposons que vous ayez un modèle de profil nommé 'Profile'
    # Renvoyer le dictionnaire de contexte
    return {
        'user_profile': profile,
        'user_activities': activities,
        'total_activities': total_activities,
        'discussion': threads,
        'no_discussion': no_discussion,
        'thread_data': thread_data,
    }

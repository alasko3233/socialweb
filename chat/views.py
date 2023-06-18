from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from chat.models import Thread

# Create your views here.


@login_required
def chat(request):
    # Récupérer tous les threads associés à l'utilisateur connecté
    threads = Thread.objects.by_user(user=request.user).prefetch_related(
        'chatmessage_thread').order_by('timestamp')

    context = {
        'Threads': threads
    }
    return render(request, 'page/chatprod.html', context)


# Le prefetch_related est une méthode de requête de Django qui permet de précharger les objets liés à une relation ManyToMany ou ForeignKey afin d'optimiser les performances de la requête.

# Dans le code donné, la ligne prefetch_related('chatmessage_thread') est utilisée pour précharger les objets ChatMessage associés à chaque thread. Cela signifie que lors de l'exécution de la requête pour récupérer les threads, Django préchargera également tous les objets ChatMessage liés à ces threads. Cela évite les requêtes supplémentaires à la base de données lors de l'accès aux objets ChatMessage dans le template ou dans le reste du code.

# En préchargeant les objets ChatMessage, les performances globales de la requête sont améliorées, car toutes les données nécessaires sont récupérées en une seule requête, plutôt que d'effectuer des requêtes individuelles pour chaque objet ChatMessage lorsque cela est nécessaire.

# Cela permet d'éviter les problèmes de latence et d'améliorer l'efficacité lors de l'affichage des informations de chat dans le template.

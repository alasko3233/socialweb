from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your models here.
User = get_user_model()


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        # Récupérer l'utilisateur à partir des arguments
        user = kwargs.get('user')
        # Définir la requête de recherche en utilisant Q pour effectuer une recherche sur plusieurs champs
        lookup = Q(first_person=user) | Q(second_person=user)
        # Filtrer les threads en fonction de la requête de recherche et supprimer les doublons
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    # Premier utilisateur dans la conversation
    first_person = models.ForeignKey(User, on_delete=models.CASCADE,
                                     null=True, blank=True, related_name='thread_first_person')
    # Deuxième utilisateur dans la conversation
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='thread_second_person')
    # Date de la dernière mise à jour du thread
    updated = models.DateTimeField(auto_now=True)
    # Date de création du thread
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        # Contrainte d'unicité pour s'assurer qu'un même thread ne peut pas être créé deux fois
        unique_together = ['first_person', 'second_person']

    def get_other_user(self, user):
        # Récupérer l'autre utilisateur dans la conversation en fonction de l'utilisateur donné
        if user == self.first_person:
            return self.second_person
        elif user == self.second_person:
            return self.first_person
        return None

    def get_last_message_by_other_user(self, user):
        # Récupérer le dernier message de l'autre utilisateur dans la conversation en fonction de l'utilisateur donné
        other_user = self.first_person if user == self.second_person else self.second_person
        # Récupérer le dernier message de la conversation filtré par l'autre utilisateur et trié par timestamp décroissant
        last_message = self.chatmessage_thread.filter(
            user=other_user).order_by('-timestamp').first()
        return last_message


class ChatMessage(models.Model):
    # Thread associé au message
    thread = models.ForeignKey(Thread, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='chatmessage_thread')
    # Utilisateur qui a envoyé le message
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    # Contenu du message
    message = models.TextField()
    # Date de création du message
    timestamp = models.DateTimeField(auto_now_add=True)

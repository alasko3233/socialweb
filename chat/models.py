from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your models here.
User = get_user_model()


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE,
                                     null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']

    def get_other_user(self, user):
        if user == self.first_person:
            return self.second_person
        elif user == self.second_person:
            return self.first_person
        return None

    def get_last_message_by_other_user(self, user):
        other_user = self.first_person if user == self.second_person else self.second_person
        last_message = self.chatmessage_thread.filter(
            user=other_user).order_by('-timestamp').first()
        return last_message


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True,
                               on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

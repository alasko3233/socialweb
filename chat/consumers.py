import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from chat.models import ChatMessage, Thread

# from chat.models import Thread, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        # Cette fonction est appelée lorsque la connexion WebSocket est établie
        print('connected', event)
        # Récupérer l'utilisateur à partir du contexte de la connexion
        user = self.scope['user']
        # Générer un nom de salon de discussion unique basé sur l'ID de l'utilisateur
        chat_room = f'user_chat_room_{user.id}'
        # Stocker le nom du salon de discussion dans l'instance du consommateur
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )  # Ajouter le canal du consommateur au groupe du salon de discussion
        await self.send({
            'type': 'websocket.accept',
        })  # Accepter la connexion WebSocket

    async def websocket_receive(self, event):
        # Réception d'un message depuis le websocket
        print('receive', event)
        received_data = json.loads(event['text'])
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        sent_to_id = received_data.get('sent_to')
        thread_id = received_data.get('thread_id')

        print(sent_by_id)
        print(sent_by_id)

        if not msg:
            print('Error no message')
            return False
        sent_by_user = await self.get_user_objects(sent_by_id)
        sent_to_user = await self.get_user_objects(sent_to_id)
        thread_obj = await self.get_thread(thread_id)
        if not sent_to_user:
            print('Error sent to user not found')
        if not sent_by_user:
            print('Error sent by user not found')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj, sent_by_user, msg)

        other_user_chat_room = f'user_chat_room_{sent_to_id}'
        self_user = self.scope['user']

        response = {
            "message": msg,
            "sent_by": self_user.id,
            'thread_id': thread_id
        }
        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response),
            }
        )

        # await self.send({
        #     'type': 'websocket.send',
        #     'text': json.dumps(response),
        # })

    async def websocket_disconnect(self, event):
        # Déconnexion du websocket
        print('disconnect', event)

    async def chat_message(self, event):
        # Envoi d'un message dans le chat
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    @database_sync_to_async
    def get_user_objects(self, user_id):
        # Récupérer un objet utilisateur de la base de données de manière asynchrone
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        # Récupérer un objet Thread de la base de données de manière asynchrone
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        # Créer un nouveau message dans le chat de manière asynchrone
        ChatMessage.objects.create(thread=thread, user=user, message=msg)

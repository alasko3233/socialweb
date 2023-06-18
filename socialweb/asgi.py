"""
ASGI config for socialweb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import chat.routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialweb.settings')

# application = get_asgi_application()
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    )
})

# get_asgi_application est une fonction utilitaire fournie par Django qui permet de charger l'application ASGI (Asynchronous Server Gateway Interface). L'ASGI est une interface standard pour les serveurs Web permettant de gérer des connexions asynchrones, telles que les connexions WebSocket.

# La fonction get_asgi_application retourne une instance de l'application Django configurée pour fonctionner avec l'ASGI. Cette application peut ensuite être utilisée par un serveur ASGI pour gérer les requêtes entrantes.

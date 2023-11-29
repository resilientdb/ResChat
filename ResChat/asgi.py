"""
ASGI config for ResChat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# config for my app0
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app0.consumers import PersonalChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ResChat.settings')

django_asgi_app = get_asgi_application()
# config for my app0 app
application = ProtocolTypeRouter({
    "http": django_asgi_app,  # HTTP requests are handled by Django
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<str:friend_nickname>/', PersonalChatConsumer.as_asgi()) # suffix of websocket path( not normal django request).
        ])
    )
})
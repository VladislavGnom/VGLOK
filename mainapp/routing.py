from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:chat_id>/', consumers.PersonalChatConsumer.as_asgi())
]
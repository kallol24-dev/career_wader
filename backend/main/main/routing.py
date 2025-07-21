from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path("ws/admin/notifications/", consumer.AdminNotificationConsumer.as_asgi()),
]
from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    re_path(r'wss/chat/(?P<friendship_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    
]
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from letter_app.routing import websocket_urlpatterns  # Importe as rotas WebSocket do seu aplicativo

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_indie.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Adicione as rotas WebSocket do seu aplicativo aqui
        )
    ),
})

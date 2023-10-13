# No arquivo filters.py do seu aplicativo
from django import template
from django.contrib.auth import get_user_model
from django.templatetags.static import static  # Importe a função 'static' para lidar com arquivos estáticos
from storage_app.models import UserProfile

register = template.Library()

@register.filter
def get_profile_image(user_profiles, username):
    try:
        user_profile = user_profiles.get(user__username=username)
        if user_profile.profile_picture:
            return user_profile.profile_picture.url
    except UserProfile.DoesNotExist:
        pass

    # Use a função 'static' para criar o URL da imagem padrão a partir do caminho relativo nos arquivos estáticos
    return static('img/whyman.png')

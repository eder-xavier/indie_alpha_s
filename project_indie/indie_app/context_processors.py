from .models import CustomUser

def user_profile(request):
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(username=request.user.username)
        return {'user_profile': user_profile}
    return {}
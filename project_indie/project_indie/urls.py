"""
URL configuration for project_indie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#urlpatterns = [
    #Rota, view responsavel, nome de referencia
    #path('', views.home, name='home'),
    #path('home/', views.home, name='list_users')
#]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('indie_app.urls')),
    path('msg/', include('letter_app.urls', namespace='letter_app')),
    path('files/', include('storage_app.urls', namespace='storage_app')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

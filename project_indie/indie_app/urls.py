from django.urls import path 
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'indie_app'

urlpatterns = [
    
    #path('endereço/', MinhaView.as_view(), name='nome-da-url')
    path('', views.home,  name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    path('register/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('main/', views.mainPage, name='main'),
    path('logout/', views.LogoutPage, name='logout'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#{% url '' %}

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
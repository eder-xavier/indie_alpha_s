

#class UserForm(forms.ModelForm):
#    password = forms.CharField(label='Senha', widget=forms.TextInput(attrs={'type': 'password'}))

#    class Meta:
#        model = User
#        fields = ['first_name', 'username', 'email', 'password']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        error_messages={
            'password_mismatch': 'As senhas não coincidem. Por favor, tente novamente.',
        }
    )

    class Meta:
        model = CustomUser
        fields = ('name', 'username', 'password1', 'password2')
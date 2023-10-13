from django import forms
from .models import Group, Message
from storage_app.models import UserProfile
from indie_app.models import CustomUser  
from django.utils.translation import gettext_lazy as _

class MessageForm(forms.Form):
   class Meta:
       model = Message
       fields = ['content']
   content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
#   attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'custom-file-input'}))

#class MessageForm(forms.ModelForm):
#    class Meta:
 #       model = Message
 #       fields = ['content', 'image', 'video', 'document']  # Adicione os campos de anexos
#
#    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Digite sua mensagem...'}))
#
#    def clean(self):
#        cleaned_data = super().clean()
 #       image = cleaned_data.get('image')
 #       video = cleaned_data.get('video')
 #       document = cleaned_data.get('document')
#
 #       if not image and not video and not document:
 #           raise forms.ValidationError('Você deve fornecer um texto, imagem, vídeo ou documento.')
#
 #       return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  
        fields = ['profile_picture', 'bio']  # Adiciona os campos que deseja exibir/editar

    profile_picture = forms.ImageField(required=False)  # Define o campo como não obrigatório

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'image', 'description']
    image = forms.ImageField(required=False)
    description = forms.CharField(max_length=639, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'group_name_class'
        self.fields['name'].widget.attrs['placeholder'] = 'Nome do grupo'
        self.fields['image'].widget.attrs['class'] = 'group_image_class'
        self.fields['description'].widget.attrs['class'] = 'group_description_class'  
        self.fields['description'].widget.attrs['placeholder'] = 'Adicione a descrição do grupo'  
        self.fields['image'].widget.attrs['class'] = 'group_image_class'
        
        

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image']
from django import forms
from .models import UserProfile, Publication, Comment
from django.utils.translation import gettext_lazy as _
from multiupload.fields import MultiFileField


class MultipleFileInput(forms.ClearableFileInput):
    template_name = 'widgets/multiple_file_input.html'

    class Media:
        js = ('js/multiple_file_input.js',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        labels = {
            'profile_picture': _('Foto de perfil'),
            'bio': _('Biografia'),
        }
        help_texts = {
            'profile_picture': _('Faça upload de uma foto de perfil (opcional).'),
        #    'bio': _('Escreva algo sobre você (opcional).'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget.attrs['class'] = 'profile_picture_class'
        self.fields['bio'].widget.attrs['class'] = 'class_bio_edit'  # Adicione a classe CSS aqui
        self.fields['bio'].widget.attrs['placeholder'] = 'Escreva sua bio'



class PublicationForm(forms.ModelForm):
    attachments = MultiFileField(
        min_num=1,
        max_file_size=1024*1024*5,  # Tamanho máximo de 5 MB por arquivo
        max_num=20,  # Número máximo de arquivos permitidos
        label='Anexos (arquivos ou pastas)',
        #help_text='Faça upload de arquivos .txt, .docx, .pdf ou pastas (opcional).',
        required=False,
    )
    
    #videos = forms.FileField(
        #label='Vídeos',
        #help_text='Faça upload de arquivos de vídeo (opcional).',
    #    required=False,
    #)

    class Meta:
        model = Publication
        fields = ['title','text', 'image', 'video', 'is_public']
        labels = {
            'title': '',
            'text': '',
            'image': 'Imagem',
            'video': 'Vídeo',
            'is_public': 'É público?',
            
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'title_class'
        self.fields['title'].widget.attrs['placeholder'] = 'Título'
        self.fields['text'].widget.attrs['class'] = 'text_class'
        self.fields['text'].widget.attrs['placeholder'] = 'Legenda'
        self.fields['image'].widget.attrs['class'] = 'image_class'
        self.fields['video'].widget.attrs['class'] = 'video_class'
        self.fields['attachments'].widget.attrs['class'] = 'attachments_class'
            

        #help_texts = {
        #    'text': 'Escreva o conteúdo da publicação.',
        #    'image': 'Faça upload de uma imagem (opcional).',
        #    'video': 'Faça upload de um vídeo (opcional).',
        #    'is_public': 'Marque esta opção se deseja tornar a publicação pública.',
        #}

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = "Adicionar Comentário"
        self.fields['text'].widget.attrs['class'] = 'comment-text'  # Adicione a classe CSS aqui

    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = "Adicionar Resposta"
        self.fields['text'].widget.attrs['class'] = 'reply-text'  # Adicione a classe CSS aqui

    class Meta:
        model = Comment
        fields = ['text']

class LikeForm(forms.Form):
    pass

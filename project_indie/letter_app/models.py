from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Funções para validar o tipo de arquivo
def validate_video(value):
    if not value.name.endswith(('.mp4', '.avi', '.mov')):
        raise ValidationError("O arquivo não é um vídeo válido.")

def validate_image(value):
    if not value.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        raise ValidationError("O arquivo não é uma imagem válida.")

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacts')
    contact = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contacted_by')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.contact.username}'



class Group(models.Model):
    name = models.CharField(max_length=99)
    description = models.CharField(max_length=639)
    image = models.ImageField(
        upload_to='group_images/', 
        blank=True, 
        null=True,
        default='default.png'
    )
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_groups', blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='groups_members', blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_groups')
    
    def __str__(self):
        return self.name

# sem libmagic
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    document = models.FileField(upload_to='message_attachments/', null=True, blank=True)
    video = models.FileField(upload_to='message_attachments/', null=True, blank=True, validators=[validate_video])
    image = models.ImageField(upload_to='message_images/', null=True, blank=True, validators=[validate_image])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'From: {self.sender.username} - To: {self.receiver.username}'

# sem libmagic
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_group_messages')
    content = models.CharField(max_length=3963)
    document = models.FileField(upload_to='message_attachments/', null=True, blank=True)
    video = models.FileField(upload_to='message_attachments/', null=True, blank=True, validators=[validate_video])
    image = models.ImageField(upload_to='message_images/', null=True, blank=True, validators=[validate_image])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Group: {self.group.name} - From: {self.sender.username}'
    


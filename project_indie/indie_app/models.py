from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    following = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followings')

    # Resto do seu modelo CustomUser

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
    
class Cripyto(models.Model):
    real_id = models.AutoField(primary_key=True)
    encrypted_id = models.CharField(max_length=64)
# Generated by Django 4.1.9 on 2023-09-12 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_publications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage_app.publication'),
        ),
    ]

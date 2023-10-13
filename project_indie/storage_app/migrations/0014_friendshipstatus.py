# Generated by Django 4.2.5 on 2023-10-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_app', '0013_friendshiprequest_delete_friendship'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendshipStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Friendship statuses',
            },
        ),
    ]
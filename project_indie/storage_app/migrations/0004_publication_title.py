# Generated by Django 4.1.9 on 2023-09-23 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_app', '0003_rename_post_comment_publication_comment_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]

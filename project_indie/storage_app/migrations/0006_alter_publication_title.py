# Generated by Django 4.1.9 on 2023-09-23 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage_app', '0005_alter_publication_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='title',
            field=models.TextField(max_length=30, null=True),
        ),
    ]

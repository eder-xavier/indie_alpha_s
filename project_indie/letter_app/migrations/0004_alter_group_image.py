# Generated by Django 4.2.6 on 2023-10-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter_app', '0003_group_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(blank=True, default='/static/img/whyman.png', null=True, upload_to='group_images/'),
        ),
    ]
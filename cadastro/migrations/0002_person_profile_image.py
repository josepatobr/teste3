# Generated by Django 5.1.3 on 2024-12-05 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/', verbose_name='profile image'),
        ),
    ]

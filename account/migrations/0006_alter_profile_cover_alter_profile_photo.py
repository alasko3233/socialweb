# Generated by Django 4.1.7 on 2023-05-29 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='users/cover/%Y/%m/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='users/profile/%Y/%m/'),
        ),
    ]

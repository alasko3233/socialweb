# Generated by Django 4.1.7 on 2023-05-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_profile_bio_profile_id_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='genre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='pays',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='telephone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='ville',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

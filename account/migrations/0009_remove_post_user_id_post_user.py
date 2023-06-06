# Generated by Django 4.1.7 on 2023-05-30 13:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0008_rename_user_post_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user_id',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

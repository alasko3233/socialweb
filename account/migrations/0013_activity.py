# Generated by Django 4.1.7 on 2023-06-13 16:51

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0012_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('content', models.TextField(blank=True)),
                ('related_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
# Generated by Django 4.1.7 on 2023-06-13 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='is_viewed',
            field=models.BooleanField(default=False),
        ),
    ]

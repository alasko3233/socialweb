# Generated by Django 4.1.7 on 2023-06-13 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_activity_is_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='other_username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

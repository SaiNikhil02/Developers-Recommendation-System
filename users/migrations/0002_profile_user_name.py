# Generated by Django 4.2.19 on 2025-02-27 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

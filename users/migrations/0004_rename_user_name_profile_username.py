# Generated by Django 4.2.19 on 2025-02-27 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_skill'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='user_name',
            new_name='username',
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-27 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_library', '0002_remove_useraccount_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]

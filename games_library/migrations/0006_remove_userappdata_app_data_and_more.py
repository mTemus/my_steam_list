# Generated by Django 4.0.2 on 2022-02-23 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games_library', '0005_alter_appdata_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userappdata',
            name='app_data',
        ),
        migrations.RemoveField(
            model_name='userappdata',
            name='collections',
        ),
        migrations.DeleteModel(
            name='AppCollection',
        ),
        migrations.DeleteModel(
            name='Collection',
        ),
        migrations.DeleteModel(
            name='UserAppData',
        ),
    ]

# Generated by Django 4.0.2 on 2022-02-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games_library', '0002_alter_developer_name_alter_publisher_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appdata',
            name='parent_app',
            field=models.IntegerField(default=0),
        ),
    ]
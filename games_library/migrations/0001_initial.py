# Generated by Django 4.0.2 on 2022-02-08 13:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AppCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppData',
            fields=[
                ('app_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=20)),
                ('parent_app', models.IntegerField(null=True)),
                ('short_desc', models.CharField(default='', max_length=500)),
                ('full_desc', models.CharField(default='', max_length=10000)),
                ('about', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageData',
            fields=[
                ('app_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('header', models.CharField(max_length=100)),
                ('background', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('app_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('comming_soon', models.BooleanField(default=False)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAppData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CMP', 'Completed'), ('PLG', 'Playing'), ('PLD', 'Planned'), ('ONH', 'On Hold'), ('DRO', 'Dropped')], default='PLG', max_length=3)),
                ('score', models.IntegerField(validators=[django.core.validators.MaxValueValidator(2022), django.core.validators.MinValueValidator(1000)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('hours_spent', models.FloatField()),
                ('app_data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata')),
                ('collections', models.ManyToManyField(through='games_library.AppCollection', to='games_library.Collection')),
            ],
        ),
        migrations.CreateModel(
            name='AppPublisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.publisher')),
            ],
        ),
        migrations.CreateModel(
            name='AppGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.genre')),
            ],
        ),
        migrations.CreateModel(
            name='AppDlc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata')),
                ('dlc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='AppDlc', to='games_library.appdata')),
            ],
        ),
        migrations.CreateModel(
            name='AppDeveloper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata')),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.developer')),
            ],
        ),
        migrations.AddField(
            model_name='appdata',
            name='categories',
            field=models.ManyToManyField(through='games_library.AppCategory', to='games_library.Category'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='developers',
            field=models.ManyToManyField(through='games_library.AppDeveloper', to='games_library.Developer'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='dlc',
            field=models.ManyToManyField(through='games_library.AppDlc', to='games_library.AppData'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='genres',
            field=models.ManyToManyField(through='games_library.AppGenre', to='games_library.Genre'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='images',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='games_library.imagedata'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='publishers',
            field=models.ManyToManyField(through='games_library.AppPublisher', to='games_library.Publisher'),
        ),
        migrations.AddField(
            model_name='appdata',
            name='release',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='games_library.release'),
        ),
        migrations.AddField(
            model_name='appcollection',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.userappdata'),
        ),
        migrations.AddField(
            model_name='appcollection',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.collection'),
        ),
        migrations.AddField(
            model_name='appcategory',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.appdata'),
        ),
        migrations.AddField(
            model_name='appcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games_library.category'),
        ),
    ]

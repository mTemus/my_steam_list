from django.db import models

from games_library.choices import GAME_STATUS_CHOICES, PLAYING
from django.core.validators import MaxValueValidator, MinValueValidator

from games_library.models import AppData


# Create your models here.

class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserAppData(models.Model):
    app_data = models.OneToOneField(AppData, on_delete=models.CASCADE)

    status = models.CharField(
        max_length = 3,
        choices = GAME_STATUS_CHOICES,
        default = PLAYING)

    score = models.IntegerField( 
        validators=[
            MaxValueValidator(2022),
            MinValueValidator(1000)
        ])
    collections = models.ManyToManyField(Collection, through="AppCollection")
    start_date = models.DateField()
    end_date = models.DateField()    
    hours_spent = models.FloatField()

    def __str__(self):
        return f"{self.app_data.app_id} - {self.app_data.name}"

class AppCollection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(UserAppData, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
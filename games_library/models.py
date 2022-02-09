from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .choices import GAME_STATUS_CHOICES, PLAYING

# Create your models here.

class Developer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ImageData(models.Model):
    app_id = models.IntegerField(primary_key=True, unique=True)
    header = models.CharField(max_length=100)
    background = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.app_id} images"

class Release(models.Model):
    app_id = models.IntegerField(primary_key=True, unique=True)
    comming_soon = models.BooleanField(default=False)
    release_date = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.app_id} release"

class AppData(models.Model):
    app_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=300)
    type = models.CharField(max_length=20)
    parent_app = models.IntegerField(default=0, null=True)
    dlc = models.ManyToManyField("self", through="AppDlc")
    short_desc = models.CharField(max_length=500, default="")
    full_desc = models.CharField(max_length=10000, default="")
    about = models.CharField(max_length=10000, default="")
    images = models.OneToOneField(ImageData, null=True, on_delete=models.CASCADE)
    developers = models.ManyToManyField(Developer, through="AppDeveloper")
    publishers = models.ManyToManyField(Publisher, through="AppPublisher")
    genres = models.ManyToManyField(Genre, through="AppGenre")
    categories = models.ManyToManyField(Category, through="AppCategory")
    release = models.OneToOneField(Release, unique=True, null=True, on_delete=models.CASCADE)

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
        return self.app_data.name



###### Through tables ######

class AppCategory(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey(AppData, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppGenre(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey(AppData, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppDeveloper(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(AppData, on_delete=models.CASCADE)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppPublisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(AppData, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class AppDlc(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(AppData, on_delete=models.CASCADE)
    dlc = models.ForeignKey(AppData, on_delete=models.CASCADE, related_name="AppDlc")

    def __str__(self):
        return self.name

class AppCollection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(UserAppData, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
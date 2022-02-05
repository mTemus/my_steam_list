from django.db import models

from .choices import GAME_STATUS_CHOICES, PLAYING

# Create your models here.

class Entity(models.Model):
    name = models.CharField(max_length=100)

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
        return self.app_id + ' images'

class Release(models.Model):
    app_id = models.IntegerField(primary_key=True, unique=True)
    comming_soon = models.BooleanField(default=False)
    release_date = models.DateField()

    def __str__(self):
        return self.app_id + ' release'

class AppEntityData(models.Model):
    app_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    parent_app = models.IntegerField()
    dlc = models.ManyToManyField("self", through="AppDlc")
    short_desc = models.CharField(max_length=500)
    full_desc = models.CharField(max_length=2000)
    about = models.CharField(max_length=2000)
    images = models.ForeignKey(ImageData, unique=True, on_delete=models.CASCADE)
    developers = models.ManyToManyField(Entity, through="AppDeveloper")
    publishers = models.ManyToManyField(Entity, through="AppPublisher")
    genres = models.ManyToManyField(Genre, through="AppGenre")
    categories = models.ManyToManyField(Category, through="AppCategory")
    release = models.ForeignKey(Release, unique=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserAppData(models.Model):
    app_data = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)

    status = models.CharField(
        max_length = 2,
        choices = GAME_STATUS_CHOICES,
        default = PLAYING)

    score = models.IntegerField(min_value=0, max_value=10)
    collections = models.ManyToManyField(Collection, through="AppCollection")
    start_date = models.DateField()
    end_date = models.DateField()    
    hours_spent = models.FloatField()

    def __str__(self):
        return self.app_data.name



###### Through tables ######

class AppCategory(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey("UserAppData", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppGenre(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey("UserAppData", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppDeveloper(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)
    developer = models.ForeignKey("Entity", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppPublisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)
    publisher = models.ForeignKey("Entity", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class AppDlc(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)
    dlc = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AppCollection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)
    collection = models.ForeignKey("Collection", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
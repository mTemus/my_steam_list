from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Entity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AppEntityData(models.Model):
    app_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    parent_app = models.IntegerField()
    dlc = models.ManyToManyField("self", through="AppDlc")
    short_desc = models.CharField(max_length=500)
    full_desc = models.CharField(max_length=2000)
    about = models.CharField(max_length=2000)
    img_header = models.CharField(max_length=100)
    img_background = models.CharField(max_length=100)
    developers = models.ManyToManyField(Entity, through="AppDeveloper")
    pbulishers = models.ManyToManyField(Entity, through="AppPublisher")
    comming_soon = models.BooleanField(default=False)
    release_date = models.DateField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserAppData(models.Model):
    app_data = models.ForeignKey("AppEntityData", on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    score = models.IntegerField(min_value=0, max_value=10)
    categories = models.ManyToManyField(Category, through="AppCategory")
    start_date = models.DateField()
    end_date = models.DateField()    
    hours_spent = models.FloatField()

    def __str__(self):
        return self.app_data.name

class AppCategory(models.Model):
    name = models.CharField(max_length=100)
    app = models.ForeignKey("UserAppData", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)

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
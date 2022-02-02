from django.db import models

# Create your models here.

class AppData(models.Model):
    app_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
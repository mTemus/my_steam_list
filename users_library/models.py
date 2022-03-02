from multiprocessing.sharedctypes import Value
from django.conf import settings
from django.db import models

from games_library.choices import GAME_STATUS_CHOICES, PLAYING
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    collections = models.ManyToManyField(Collection, through="AppCollection")
    start_date = models.DateField()
    end_date = models.DateField()    
    hours_spent = models.FloatField()

    def __str__(self):
        return f"{self.app_data.app_id} - {self.app_data.name}"

class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("No email address")

        if not username:
            raise ValueError("No username")

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(username, email, password, **extra_fields)

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    
    apps = models.ManyToManyField(UserAppData, through="UserApps")
    
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

class AppCollection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    app = models.ForeignKey(UserAppData, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserApps(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    app = models.ForeignKey(UserAppData, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
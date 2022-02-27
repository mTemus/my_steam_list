from multiprocessing.sharedctypes import Value
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
    def create_user(self, username, email, is_staff, password=None):
        if not email:
            raise ValueError("No email address")

        if not username:
            raise ValueError("No username")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.is_staff = is_staff

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, is_staff, password=None):

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, is_staff, password)
        user.is_superuser = True
        user.is_staff = is_staff
        user.save()
        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    apps = models.ManyToManyField(UserAppData, through="UserApps")
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'is_staff']

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
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    app = models.ForeignKey(UserAppData, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
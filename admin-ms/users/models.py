from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    admin = models.CharField(max_length=25,unique=True)
    password = models.CharField(max_length=15)
    domain = models.CharField(max_length=15,default="foodtruck")
    username = None

    USERNAME_FIELD = 'admin'
    REQUIRED_FIELDS = []


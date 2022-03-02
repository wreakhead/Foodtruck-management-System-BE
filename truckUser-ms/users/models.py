
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Truck(AbstractUser):
    truckNo = models.CharField(max_length=25,unique=True)
    creator = models.IntegerField()
    password = models.CharField(max_length=15)
    disabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = None
    USERNAME_FIELD = 'truckNo'
    REQUIRED_FIELDS = []
    

    

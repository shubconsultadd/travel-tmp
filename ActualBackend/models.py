import datetime

from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime

ROLE_CHOICES = (
    ("user", "user"),
    ("admin", "admin"),
)



class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=100, unique=True, blank=False)
    role = models.CharField(max_length=28, choices=ROLE_CHOICES, default="user")

    USERNAME_FIELD = 'username'


class TravelPlans(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    price = models.FloatField(blank=False)
    image = models.ImageField(upload_to='travel_plan_images/', blank=False)
    start_date = models.DateField()
    end_date = models.DateField()
    registered_admin_id = models.IntegerField(blank=False)
    registered_plans = models.ManyToManyField(User, through='RegisteredPlans')


class RegisteredPlans(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    planID = models.ForeignKey(TravelPlans, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('userID', 'planID')


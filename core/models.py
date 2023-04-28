from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    
    gender = models.CharField(max_length=30, blank=True, null=True, choices=GENDER)

    def __str__(self):
        return self.gender

from typing import List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone

class User(AbstractUser):
    image_url=models.URLField()
    
class BlogPost(models.Model):
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=200000000 , default="")
    posted_by=models.ForeignKey(User,on_delete=CASCADE,related_name="postedby")
    closed = models.BooleanField(default=False)
    def __str__(self) :
        return self.title

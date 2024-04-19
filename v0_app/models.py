from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000)


class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000)
    cook_steps = models.TextField()
    ingredients = models.TextField()
    cook_time = models.TimeField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='other')




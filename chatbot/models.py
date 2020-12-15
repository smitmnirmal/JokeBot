from django.db import models

# Create your models here.
class Jokes(models.Model):
    joke = models.TextField()
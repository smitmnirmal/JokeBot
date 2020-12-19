from django.db import models

# Create your models here.
class Jokes(models.Model):
    person_name = models.CharField(max_length=30, null=True)
    joke = models.TextField()
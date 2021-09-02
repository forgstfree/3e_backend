from django.db import models

# Create your models here.
class UserMathModel(models.Model):
    name = models.CharField(max_length=400)
    expression = models.TextField()
    coefficient = models.CharField(max_length=400)
    variable = models.CharField(max_length=400)
    desc = models.TextField()
    remake = models.CharField(max_length=600)
from django.db import models

# Create your models here.
class DumpModelToDelete(models.Model):
    column1 = models.CharField(max_length=100)
    column2title = models.CharField(max_length=100)

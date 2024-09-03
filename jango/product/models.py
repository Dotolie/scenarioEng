from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    cost = models.IntegerField()

    def __str__(self):
        return self.name

class MyModel(models.Model):
    contents = models.CharField(max_length=100)
    settings = models.TextField(null=True)
    conditions = models.TextField(null=True)
    results = models.TextField(null=True)
    
    def __str__(self):
        return self.contents
    
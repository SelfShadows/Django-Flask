from django.db import models

# Create your models here.


class Note(models.Model):
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=128)
    markdown = models.CharField(max_length=128)
    create_time = models.DateField(auto_now=True)
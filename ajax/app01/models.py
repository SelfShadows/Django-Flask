from django.db import models

# Create your models here.


class Persen(models.Model):
    name = models.CharField(null=False, max_length=64, unique=True)
    age = models.IntegerField()
    # birthday = models.DateField(auto_now_add=True)

    def __str__(self):
        return "<Person object : {}>".format(self.name)

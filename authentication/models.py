from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(null=False, max_length=200)
    email = models.EmailField(null=False, max_length=200)
    password = models.CharField(null=False, max_length=200)

    def __str__(self):
        return self.username
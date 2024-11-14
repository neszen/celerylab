from django.db import models

class UserData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.CharField(max_length=100)

    def __str__(self):
        return self.name

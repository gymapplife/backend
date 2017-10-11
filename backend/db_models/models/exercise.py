from django.db import models


class Exercise(models.Model):

    name = models.CharField(max_length=32)
    primary_muscle = models.CharField(max_length=16)

    def __str__(self):
        return self.name

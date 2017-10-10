from django.db import models


class WorkoutProgram(models.Model):

    name = models.CharField(max_length=64)
    length = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name} ({self.length} days)'

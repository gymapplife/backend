from django.db import models


class AbstractWorkoutProgram(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=64)
    length = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.name} ({self.length} days)'

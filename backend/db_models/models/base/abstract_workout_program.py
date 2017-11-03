from django.db import models


class AbstractWorkoutProgram(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=32)
    length = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=256, blank=True, default='')

    def __str__(self):
        return f'{self.name} ({self.length} days)'

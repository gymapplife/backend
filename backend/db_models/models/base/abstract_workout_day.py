from db_models.models.exercise import Exercise
from django.db import models


class AbstractWorkoutDay(models.Model):

    class Meta:
        abstract = True

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
    )

    @property
    def exercise_name(self):
        return self.exercise.name

    day = models.PositiveSmallIntegerField()
    week = models.PositiveSmallIntegerField()
    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

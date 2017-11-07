from db_models.models.day_of_week import DayOfWeek
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

    day = models.PositiveSmallIntegerField(
        db_index=True,
    )

    day_of_week = models.ForeignKey(DayOfWeek)

    @property
    def day_of_week_name(self):
        return self.day_of_week.name

    sets = models.PositiveSmallIntegerField()
    reps = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()

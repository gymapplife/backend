from db_models.models.day_of_week import DayOfWeek
from db_models.models.exercise import Exercise
from db_models.validators import validate_comma_separated_ints
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

    # Comma seperated string
    # eg. 5,5,5,5,5
    # Idk why anyone would want 64 chars worth, but w.e
    reps = models.CharField(
        max_length=64,
        validators=[validate_comma_separated_ints],
    )

    # Comma seperated string
    # eg. 135,135,255,255,255
    weights = models.CharField(
        max_length=128,
        validators=[validate_comma_separated_ints],
    )

    @property
    def sets(self):
        return len(self.reps.split(','))

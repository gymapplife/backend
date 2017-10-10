from db_models.models.profile import Profile
from db_models.models.workout_day import WorkoutDay
from db_models.validators import validate_comma_separated_ints
from django.db import models


class CustomWorkoutDay(models.Model):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        db_index=True,
    )

    @property
    def program(self):
        return self.workout_day.program

    @property
    def exercise(self):
        return self.workout_day.exercise

    @property
    def day(self):
        return self.workout_day.day

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

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

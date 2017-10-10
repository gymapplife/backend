from db_models.models.exercise import Exercise
from db_models.models.workout_program import WorkoutProgram
from db_models.validators import validate_comma_separated_ints
from django.db import models


class WorkoutDay(models.Model):

    workout_program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        db_index=True,
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
    )

    day = models.PositiveSmallIntegerField(
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

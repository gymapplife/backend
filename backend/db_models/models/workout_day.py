from db_models.models.base.abstract_workout_day import AbstractWorkoutDay
from db_models.models.workout_program import WorkoutProgram
from django.db import models


class WorkoutDay(AbstractWorkoutDay):

    workout_program = models.ForeignKey(
        WorkoutProgram,
        on_delete=models.CASCADE,
        db_index=True,
    )

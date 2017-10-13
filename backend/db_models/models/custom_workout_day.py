from db_models.models.base.abstract_workout_day import AbstractWorkoutDay
from db_models.models.custom_workout_program import CustomWorkoutProgram
from django.db import models


class CustomWorkoutDay(AbstractWorkoutDay):

    workout_program = models.ForeignKey(
        CustomWorkoutProgram,
        on_delete=models.CASCADE,
        db_index=True,
    )

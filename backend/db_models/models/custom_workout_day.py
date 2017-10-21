from db_models.models.base.abstract_workout_day import AbstractWorkoutDay
from db_models.models.custom_workout_program import CustomWorkoutProgram
from django.db import models


class CustomWorkoutDayException(Exception):

    def __init__(self, errors):
        self.errors = errors


class CustomWorkoutDay(AbstractWorkoutDay):

    workout_program = models.ForeignKey(
        CustomWorkoutProgram,
        on_delete=models.CASCADE,
        db_index=True,
    )

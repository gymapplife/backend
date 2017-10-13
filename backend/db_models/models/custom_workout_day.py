from db_models.models.base.abstract_workout_day import AbstractWorkoutDay
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.profile import Profile
from django.db import models


class CustomWorkoutDay(AbstractWorkoutDay):

    workout_program = models.ForeignKey(
        CustomWorkoutProgram,
        on_delete=models.CASCADE,
        db_index=True,
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

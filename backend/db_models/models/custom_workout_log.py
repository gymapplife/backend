from db_models.models.base.abstract_workout_log import (
    AbstractWorkoutLog
)
from db_models.models.custom_workout_day import CustomWorkoutDay
from django.db import models


class CustomWorkoutLog(AbstractWorkoutLog):

    workout_day = models.OneToOneField(
        CustomWorkoutDay,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
    )

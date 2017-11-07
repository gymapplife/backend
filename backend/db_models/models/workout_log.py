from db_models.models.base.abstract_workout_log import (
    AbstractWorkoutLog
)
from db_models.models.workout_day import WorkoutDay
from django.db import models


class WorkoutLog(AbstractWorkoutLog):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
        blank=True,
    )

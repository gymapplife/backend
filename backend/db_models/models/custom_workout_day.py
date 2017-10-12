from db_models.models.profile import Profile
from db_models.models.workout_day import WorkoutDay
from django.db import models


class CustomWorkoutDay(WorkoutDay):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

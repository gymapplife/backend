from db_models.models.base.abstract_workout_program import (
    AbstractWorkoutProgram
)
from db_models.models.profile import Profile
from django.db import models


class CustomWorkoutProgram(AbstractWorkoutProgram):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

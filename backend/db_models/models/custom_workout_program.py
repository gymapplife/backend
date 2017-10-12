from db_models.models.profile import Profile
from db_models.models.workout_program import WorkoutProgram
from django.db import models


class CustomWorkoutProgram(WorkoutProgram):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

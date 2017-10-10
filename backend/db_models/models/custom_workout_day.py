from db_models.models.abstract.sets_reps_weights import SetsRepsWeights
from db_models.models.exercise import Exercise
from db_models.models.profile import Profile
from db_models.models.workout_program import WorkoutProgram
from django.db import models


class CustomWorkoutDay(SetsRepsWeights):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

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

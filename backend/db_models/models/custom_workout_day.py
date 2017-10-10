from db_models.models.abstract.sets_reps_weights import SetsRepsWeights
from db_models.models.profile import Profile
from db_models.models.workout_day import WorkoutDay
from django.db import models


class CustomWorkoutDay(SetsRepsWeights):

    workout_day = models.ForeignKey(
        WorkoutDay,
        on_delete=models.CASCADE,
        db_index=True,
    )

    @property
    def program(self):
        return self.workout_day.program

    @property
    def exercise(self):
        return self.workout_day.exercise

    @property
    def day(self):
        return self.workout_day.day

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

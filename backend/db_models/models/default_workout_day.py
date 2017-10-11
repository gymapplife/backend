from db_models.models.abstract.workout_day import WorkoutDay
from db_models.models.exercise import Exercise
from db_models.models.workout_program import WorkoutProgram
from django.db import models


class DefaultWorkoutDay(WorkoutDay):

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

from db_models.models.workout_program import WorkoutProgram
from django.db import models


class DefaultWorkoutProgram(models.Model):

    workout_program = models.OneToOneField(
        WorkoutProgram,
        primary_key=True,
        on_delete=models.CASCADE,
    )

    @property
    def name(self):
        return self.workout_program.name

    @property
    def length(self):
        return self.workout_program.length

    def __str__(self):
        return self.workout_program.__str__()

from db_models.models.exercise import Exercise
from db_models.models.profile import Profile
from django.db import models


class PersonalRecord(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        db_index=True,
    )

    weight = models.PositiveSmallIntegerField()

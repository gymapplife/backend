from db_models.models.exercise import Exercise
from db_models.models.profile import Profile
from django.db import models


class AbstractMedia(models.Model):

    class Meta:
        abstract = True

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

    title = models.CharField(max_length=64)

    s3_url = models.CharField(max_length=1024)

    def __str__(self):
        return f'{self.exercise.name} {self.__class__.__name__}'

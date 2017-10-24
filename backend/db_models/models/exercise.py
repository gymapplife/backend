from db_models.models.public_photo import PublicPhoto
from db_models.models.public_video import PublicVideo
from django.db import models


class Exercise(models.Model):

    name = models.CharField(max_length=32)
    primary_muscle = models.CharField(max_length=16)

    photo = models.OneToOneField(
        PublicPhoto,
        on_delete=models.SET_NULL,
        null=True,
    )

    video = models.OneToOneField(
        PublicVideo,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name

from db_models.models.base.abstract_media import AbstractMedia
from db_models.models.profile import Profile
from django.db import models
from lib.s3 import S3


class AbstractUploadedMedia(AbstractMedia):

    class Meta:
        abstract = True

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

    def upload_url(self):
        return S3.get_upload_url(self.s3_bucket, self.s3_key)

import uuid

from django.db import models
from lib.s3 import S3


class AbstractMedia(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=64)

    s3_bucket = None
    s3_key = models.UUIDField(default=uuid.uuid4, editable=False)

    def download_url(self):
        return S3.get_download_url(self.s3_bucket, self.s3_key)

    def delete(self):
        S3.delete(self.s3_bucket, self.s3_key)
        super().delete()

    def __str__(self):
        return f'{self.__class__.__name__}: {self.name}'

from db_models.models.base.abstract_uploaded_media import AbstractUploadedMedia


class UploadedPhoto(AbstractUploadedMedia):

    s3_bucket = 'gymapplife-uploaded-photo'

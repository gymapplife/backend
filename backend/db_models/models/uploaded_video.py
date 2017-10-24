from db_models.models.base.abstract_uploaded_media import AbstractUploadedMedia


class UploadedVideo(AbstractUploadedMedia):

    s3_bucket = 'uploaded-video'

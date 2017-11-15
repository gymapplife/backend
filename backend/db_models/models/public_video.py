from db_models.models.base.abstract_media import AbstractMedia


class PublicVideo(AbstractMedia):

    s3_bucket = 'gymapplife-public-video'

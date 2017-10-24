from db_models.models.base.abstract_media import AbstractMedia


class PublicPhoto(AbstractMedia):

    s3_bucket = 'public-photo'

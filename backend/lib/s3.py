import abc

from backend.settings import DEBUG


class _AbstractS3(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_upload_url(self, bucket, key):
        pass

    @abc.abstractmethod
    def get_download_url(self, bucket, key):
        pass

    @abc.abstractmethod
    def delete(self, bucket, key):
        pass


class _MockS3(_AbstractS3):

    def get_upload_url(self, bucket, key):
        return f'upload {bucket} {key}'

    def get_download_url(self, bucket, key):
        return f'download {bucket} {key}'

    def delete(self, bucket, key):
        pass


class _S3(_AbstractS3):
    """George: boto3.readthedocs.io/en/latest/reference/services/s3.html
    Look for `presigned`
    """

    def get_upload_url(self, bucket, key):
        pass

    def get_download_url(self, bucket, key):
        pass

    def delete(self, bucket, key):
        pass


S3 = _MockS3() if DEBUG else _S3()

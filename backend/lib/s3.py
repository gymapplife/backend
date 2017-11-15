import abc
import boto3

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
        return f'upload | {bucket} | {key}'

    def get_download_url(self, bucket, key):
        return f'download | {bucket} | {key}'

    def delete(self, bucket, key):
        pass


class _S3(_AbstractS3):
    """George: boto3.readthedocs.io/en/latest/reference/services/s3.html
    Look for `presigned`
    """

    def __init__(self):
        self.client = boto3.client('s3')

    def get_upload_url(self, bucket, key):
        resp = self.client.generate_presigned_post(
            Bucket=bucket,
            Key=key
        )
        return resp

    def get_download_url(self, bucket, key):
        """Please return None if does not exist.
        """
        try:
            self.client.head_object(Bucket=bucket, Key=key)
        except:
            return None

        resp = self.client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket,
                'Key': key
            },
            HttpMethod='GET'
        )
        return resp

    def delete(self, bucket, key):
        self.client.delete_object(
            Bucket=bucket,
            Key=key
        )


S3 = _MockS3() if DEBUG else _S3()

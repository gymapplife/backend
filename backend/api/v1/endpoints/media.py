from api.views import ProfileAuthedAPIView
from db_models.models.public_photo import PublicPhoto
from db_models.models.public_video import PublicVideo
from db_models.models.uploaded_photo import UploadedPhoto
from db_models.models.uploaded_video import UploadedVideo
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from utils.models import get_model_for_profile
from utils.query import get_query_switches


class DownloadMediaSerializer(serializers.ModelSerializer):

    class Meta:
        # Quite a bit of a hack. Cannot put abstract models here.
        # Since these fields are shared, just use PublicPhoto /shrug
        model = PublicPhoto
        fields = (
            'id',
            'name',
            'download_url',
        )
        read_only_fields = ('download_url',)


class UploadedPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedPhoto
        fields = (
            'id',
            'name',
            'profile',
            'upload_info',
        )
        read_only_fields = ('upload_info',)


class UploadedVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UploadedVideo
        fields = (
            'id',
            'name',
            'profile',
            'upload_info',
        )
        read_only_fields = ('upload_info',)


class MediasView(ProfileAuthedAPIView):

    def get(self, request):
        """Get S3 urls to download media from

        #### Query Parameters
        * public_photo (optional)
        * public_video (optional)
        * uploaded_photo (optional)
        * uploaded_video (optional)

        `?public_photo` will return all public photos.

        `?public_video` will return all public photos.

        `?uploaded_photo` will return all photos available to the user.

        `?uploaded_video` will return all videos available to the user.

        You can `&` parameters together.
        No parameters is same as having all parameters.

        #### Sample Response
        ```
        {
            "public_photo": [],
            "public_video": [],
            "uploaded_photo": [
                {
                    "id": 1,
                    "name": "nameee",
                    "download_url": "https://bopeng.io/assets/axongc.png"
                }
            ],
            "uploaded_video": []
        }
        ```
        """
        query_switches = get_query_switches(
            request.query_params,
            [
                'public_photo',
                'public_video',
                'uploaded_photo',
                'uploaded_video',
            ],
            all_true_on_none=True,
        )

        response_dict = {}

        if 'public_photo' in query_switches:
            response_dict['public_photo'] = DownloadMediaSerializer(
                PublicPhoto.objects.all(),
                many=True,
            ).data

        if 'public_video' in query_switches:
            response_dict['public_video'] = DownloadMediaSerializer(
                PublicVideo.objects.all(),
                many=True,
            ).data

        if 'uploaded_photo' in query_switches:
            response_dict['uploaded_photo'] = DownloadMediaSerializer(
                request.profile.uploadedphoto_set.all(),
                many=True,
            ).data

        if 'uploaded_video' in query_switches:
            response_dict['uploaded_video'] = DownloadMediaSerializer(
                request.profile.uploadedvideo_set.all(),
                many=True,
            ).data

        return Response(response_dict)

    def post(self, request):
        """Get an S3 url to upload media to

        #### Body Parameters
        * name: string

        #### Query Parameters
        * photo (or video)
        * video (or photo)

        `?photo` will return a photo upload url.

        `?video` will return a video upload url.

        `photo` takes precedence over `video`.

        #### Sample Response
        ```
        {
            "id": 2,
            "name": "nameee",
            "upload_info": {
                "url": "https://gymapplife-uploaded-photo.s3.amazonaws.com/",
                "fields": {
                    "key": "9842a2c8-14fd-4fe7-b6c7-b3a99d0d4a6c",
                    "AWSAccessKeyId": "AWSAccessKeyId",
                    "policy": "policy",
                    "signature": "signature"
                }
            }
        }
        ```
        """
        query_switches = get_query_switches(
            request.query_params,
            ['photo', 'video'],
            raise_on_none=True,
        )

        if 'photo' in query_switches:
            UploadedSerializer = UploadedPhotoSerializer
        elif 'video' in query_switches:
            UploadedSerializer = UploadedVideoSerializer

        if request.data:
            request.data._mutable = True
            request.data['profile'] = request.profile.pk
            request.data._mutable = False

        serializer = UploadedSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = dict(serializer.data)
            data.pop('profile', None)
            return Response(data, status=status.HTTP_201_CREATED)

        errors = dict(serializer.errors)
        errors.pop('profile', None)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class MediaView(ProfileAuthedAPIView):

    def get(self, request, pk):
        """Get an S3 url to download media from

        #### Query Parameters
        * photo (or video)
        * video (or photo)

        `?photo` will return a photo download url.

        `?video` will return a video download url.

        `photo` takes precedence over `video`.

        #### Sample Response
        ```
        {
            "id": 1,
            "name": "nameee",
            "download_url": "https://bopeng.io/assets/axongc.png"
        }
        ```
        """
        query_switches = get_query_switches(
            request.query_params,
            ['photo', 'video'],
            raise_on_none=True,
        )

        if 'photo' in query_switches:
            media = get_model_for_profile(
                UploadedPhoto,
                request.profile,
                pk=pk,
            )
        elif 'video' in query_switches:
            media = get_model_for_profile(
                UploadedVideo,
                request.profile,
                pk=pk,
            )

        return Response(DownloadMediaSerializer(media).data)

    def delete(self, request, pk):
        """Delete media

        #### Query Parameters
        * photo (or video)
        * video (or photo)

        `?photo` will delete photo of given id.

        `?video` will delete video of given id.

        `photo` takes precedence over `video`.
        """
        query_switches = get_query_switches(
            request.query_params,
            ['photo', 'video'],
            raise_on_none=True,
        )

        if 'photo' in query_switches:
            media = get_model_for_profile(
                UploadedPhoto,
                request.profile,
                pk=pk,
            )
        elif 'video' in query_switches:
            media = get_model_for_profile(
                UploadedVideo,
                request.profile,
                pk=pk,
            )

        media.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

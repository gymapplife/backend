from api.views import ProfileAuthedAPIView
from db_models.models.photo import Photo
from db_models.models.video import Video
from django.http import Http404
from django.shortcuts import get_object_or_404
from lib import s3
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class CreatePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = (
            'id',
            'profile',
            'exercise',
            'title',
            's3_url',
        )


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = (
            'id',
            'exercise',
            'title',
            's3_url',
        )
        read_only_fields = ('s3_url',)


class CreateVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'id',
            'profile',
            'exercise',
            'title',
            's3_url',
        )


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'id',
            'exercise',
            'title',
            's3_url',
        )
        read_only_fields = ('s3_url',)


class MediasView(ProfileAuthedAPIView):

    def get(self, request):
        """Get S3 urls to download media from

        #### Query Parameters
        * photo: 1 (optional)
        * video: 1 (optional)

        No query parameters will return nothing.

        `?photo` will return all photos available to the user.

        `?video` will return all videos available to the user.

        `?photo&video` will return both types.


        #### Sample Response
        ```
        {
            "photo": [
                {
                    "id": 2,
                    "exercise": 1,
                    "title": "swag",
                    "s3_url": "MOCK_S3_DOWNLOAD_URL"
                }
            ],
            "video": [
                {
                    "id": 4,
                    "exercise": 1,
                    "title": "swag",
                    "s3_url": "MOCK_S3_DOWNLOAD_URL"
                }
            ]
        }
        ```
        """
        response_dict = {}

        if 'photo' in request.query_params:
            datas = PhotoSerializer(
                request.profile.photo_set.all(),
                many=True,
            ).data
            for data in datas:
                # TODO: Delete model from DB if S3 doesn't exist
                data['s3_url'] = s3.get_download_url(data['s3_url'])
            response_dict['photo'] = datas

        if 'video' in request.query_params:
            datas = VideoSerializer(
                request.profile.video_set.all(),
                many=True,
            ).data
            for data in datas:
                data['s3_url'] = s3.get_download_url(data['s3_url'])
            response_dict['video'] = datas

        return Response(response_dict)

    def post(self, request):
        """Get an S3 url to upload media to

        #### Body Parameters
        * title: string
        * exercise: integer

        #### Sample Response
        ```
        {
            "id": 5,
            "exercise": 1,
            "title": "swag",
            "s3_url": "MOCK_S3_UPLOAD_URL"
        }
        ```
        """
        if 'photo' in request.query_params:
            CreateSerializer = CreatePhotoSerializer
        elif 'video' in request.query_params:
            CreateSerializer = CreateVideoSerializer
        else:
            return Response(
                {
                    'detail': 'One of `photo` or `video` '
                    + 'query parameter is required',
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data:
            request.data._mutable = True
            request.data['profile'] = request.profile.pk
            request.data['s3_url'] = s3.create_bucket()
            request.data._mutable = False

        serializer = CreateSerializer(data=request.data)

        s3_upload_url = s3.get_upload_url(request.data['s3_url'])

        if serializer.is_valid():
            serializer.save()
            data = dict(serializer.data)
            data['s3_url'] = s3_upload_url
            data.pop('profile', None)
            return Response(data, status=status.HTTP_201_CREATED)

        errors = dict(serializer.errors)
        errors.pop('profile', None)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class MediaView(ProfileAuthedAPIView):

    def delete(self, request, pk):
        """Delete media

        #### Query Parameters
        * photo (or video)
        * video (or photo)
        """
        if 'photo' in request.query_params:
            media = get_object_or_404(Photo, pk=pk)
            if media.profile != request.profile:
                raise Http404()
        elif 'video' in request.query_params:
            media = get_object_or_404(Video, pk=pk)
            if media.profile != request.profile:
                raise Http404()
        else:
            return Response(
                {
                    'detail': 'One of `photo` or `video` '
                    + 'query parameter is required',
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        s3.delete_bucket(media.s3_url)
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

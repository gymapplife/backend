from api.v1.endpoints.media import DownloadMediaSerializer
from api.views import ProfileAuthedAPIView
from db_models.models.exercise import Exercise
from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = (
            'id',
            'name',
            'primary_muscle',
            'photo',
            'video',
        )

    photo = DownloadMediaSerializer()
    video = DownloadMediaSerializer()


class ExercisesView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of exercises

        #### Sample Response
        ```
        [
            ...
            {
                "id": 48,
                "name": "Incline Dumbbell Curl",
                "primary_muscle": "Arms",
                "photo": null,
                "video": null
            },
            {
                "id": 49,
                "name": "Barbell Curl",
                "primary_muscle": "Arms",
                "photo": {
                    "id": 1,
                    "name": "asdasdsa",
                    "download_url": "some url"
                },
                "video": null
            }
        ]
        ```
        """
        return Response(
            ExerciseSerializer(
                Exercise.objects.all(),
                many=True,
            ).data,
        )


class ExerciseView(ProfileAuthedAPIView):

    def get(self, request, pk):
        """Get an exercise

        #### Sample Response
        ```
        {
            "id": 49,
            "name": "Barbell Curl",
            "primary_muscle": "Arms",
            "photo": {
                "id": 1,
                "name": "asdasdsa",
                "download_url": "some url"
            },
            "video": null
        }
        ```
        """
        try:
            return Response(
                ExerciseSerializer(
                    Exercise.objects.get(pk=pk),
                ).data,
            )
        except Exercise.DoesNotExist:
            raise Http404()

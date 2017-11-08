from api.views import ProfileAuthedAPIView
from db_models.models.personal_record import PersonalRecord
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class PersonalRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalRecord
        fields = (
            'id',
            'profile',
            'exercise',
            'weight',
        )


class PersonalRecordView(ProfileAuthedAPIView):

    def get(self, request):
        """Get all of your personal records

        #### Sample Response
        ```
        {
            "1": 1,
            "2": 10
        }
        ```

        exercise ID : weight
        """
        data = PersonalRecordSerializer(
            PersonalRecord.objects.filter(profile=request.profile).all(),
            many=True,
        ).data
        response_dict = {}
        for record in data:
            response_dict[record['exercise']] = record['weight']
        return Response(response_dict)

    def put(self, request):
        """Create or patch a personal record

        #### Body Parameters
        * exercise: integer
        * weight: integer

        #### Sample Response
        ```
        {
            "id": 2,
            "profile": 1,
            "exercise": 2,
            "weight": 10
        }
        ```
        """
        if request.data:
            request.data._mutable = True
            request.data['profile'] = request.profile.pk
            request.data._mutable = False

        serializer = PersonalRecordSerializer(data=request.data)

        if not serializer.is_valid():
            errors = dict(serializer.errors)
            errors.pop('profile', None)

            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            personal_record = PersonalRecord.objects.get(
                profile=request.profile,
                exercise=request.data['exercise'],
            )
        except PersonalRecord.DoesNotExist:
            personal_record = None

        serializer = PersonalRecordSerializer(
            personal_record,
            data=request.data,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        raise Exception('Should never happen.')

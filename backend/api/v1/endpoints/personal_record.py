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

    @staticmethod
    def create_update(data, increase_only=True):
        try:
            personal_record = PersonalRecord.objects.get(
                profile=data['profile'],
                exercise=data['exercise'],
            )
        except PersonalRecord.DoesNotExist:
            personal_record = None

        serializer = PersonalRecordSerializer(
            personal_record,
            data=data,
        )

        if serializer.is_valid():
            if increase_only and (
                personal_record
                and personal_record.weight >= int(data['weight'])
            ):
                return PersonalRecordSerializer(
                    personal_record,
                ).data, False
            serializer.save()
            if personal_record:
                return serializer.data, False
            else:
                return serializer.data, True

        raise Exception('Should never happen.')

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

        data, created = PersonalRecordView.create_update(
            request.data,
            increase_only=False,
        )

        if created:
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(data)

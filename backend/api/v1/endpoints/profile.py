from api.views import AuthedAPIView
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.profile import Profile
from db_models.models.profile import SelectWorkoutProgramException
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from utils.response import NoProfileForbiddenResponse


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'goal',
            'experience',
            'weight',
            'height',
            'current_workout_program',
            'current_custom_workout_program',
        )


class ProfileCreateSerializer(ProfileSerializer):

    id = serializers.IntegerField()


class ProfileView(AuthedAPIView):

    def get(self, request):
        """Get profile

        #### Sample Response
        ```
        {
            "id": integer,
            "goal": string,
            "experience": string,
            "weight": integer,
            "height": integer,
            "current_workout_program": integer|null,
            "current_custom_workout_program": integer|null
        }
        ```
        """
        try:
            profile = Profile.objects.get(id=request.fb_id)
        except:
            return NoProfileForbiddenResponse()

        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    def post(self, request):
        """Create profile

        #### Body Parameters
        * goal: string
        * experience: string
        * weight: integer
        * height: integer
        * current_workout_program: integer (optional)

        #### Sample Response
        ```
        {
            "id": integer,
            "goal": string,
            "experience": string,
            "weight": integer,
            "height": integer,
            "current_workout_program": integer|null,
            "current_custom_workout_program": null
        }
        ```
        """
        try:
            Profile.objects.get(id=request.fb_id)
            return Response(
                {'id': f'"{request.fb_id}" already in use.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            pass

        if request.data:
            if 'current_custom_workout_program' in request.data:
                return Response(
                    {
                        'current_custom_workout_program': 'Can not select '
                        + 'on profile creation.',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.data._mutable = True
            request.data['id'] = request.fb_id
            request.data._mutable = False

        serializer = ProfileCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = dict(serializer.errors)
        errors.pop('id', None)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update profile

        #### Body Parameters
        * goal: string (optional)
        * experience: string (optional)
        * weight: integer (optional)
        * height: integer (optional)
        * current_workout_program: integer (optional)
        * current_custom_workout_program: integer (optional)

        Only one of `current_workout_program`
        and `current_custom_workout_program` may be populated.

        To switch types, explicitly set one to `null`.

        #### Sample Response
        ```
        {
            "id": integer,
            "goal": string,
            "experience": string,
            "weight": integer,
            "height": integer,
            "current_workout_program": integer|null,
            "current_custom_workout_program": integer|null
        }
        ```
        """
        try:
            profile = Profile.objects.get(id=request.fb_id)
        except:
            return NoProfileForbiddenResponse()

        if request.data and 'current_custom_workout_program' in request.data:
            pk = request.data['current_custom_workout_program']
            try:
                if not CustomWorkoutProgram.objects.get(
                    id=pk,
                ).profile.id == profile.id:
                    raise Exception()
            except:
                msg = f'Invalid pk "{pk}" - object does not exist.'
                return Response(
                    {
                        'current_custom_workout_program': msg,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except SelectWorkoutProgramException as e:
                s = str(e)
                return Response(
                    {
                        'current_workout_program': s,
                        'current_custom_workout_program': s,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete profile
        """
        try:
            profile = Profile.objects.get(id=request.fb_id)
        except:
            return NoProfileForbiddenResponse()

        profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

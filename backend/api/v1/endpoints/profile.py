from api.views import AuthedAPIView
from db_models.models.profile import Profile
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
            "current_workout_program": integer|null
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

        #### Parameters
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
            "current_workout_program": integer|null
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
            request.data._mutable = True
            request.data['id'] = request.fb_id
            request.data._mutable = False

        serializer = ProfileCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        """Update profile

        #### Parameters
        * goal: string (optional)
        * experience: string (optional)
        * weight: integer (optional)
        * height: integer (optional)
        * current_workout_program: integer (optional)

        #### Sample Response
        ```
        {
            "id": integer,
            "goal": string,
            "experience": string,
            "weight": integer,
            "height": integer,
            "current_workout_program": integer|null
        }
        ```
        """
        try:
            profile = Profile.objects.get(id=request.fb_id)
        except:
            return NoProfileForbiddenResponse()

        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
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

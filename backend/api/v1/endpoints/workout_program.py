from api.views import ProfileAuthedAPIView
from db_models.models.workout_program import WorkoutProgram
from rest_framework import serializers
from rest_framework.response import Response


class WorkoutProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutProgram
        fields = (
            'id',
            'name',
            'length',
        )


class WorkoutProgramsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of workout programs

        #### Sample Response
        ```

        ```
        """
        workout_programs = WorkoutProgram.objects.all()

        serializer = WorkoutProgramSerializer(workout_programs, many=True)

        return Response(serializer.data)

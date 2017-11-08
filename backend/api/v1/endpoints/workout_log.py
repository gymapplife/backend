from api.views import ProfileAuthedAPIView
from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.custom_workout_log import CustomWorkoutLog
from db_models.models.workout_day import WorkoutDay
from db_models.models.workout_log import WorkoutLog
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from utils.query import get_query_switches


class WorkoutLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutLog
        fields = (
            'id',
            'profile',
            'created',
            'workout_day',
            'reps',
        )


class CustomWorkoutLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomWorkoutLog
        fields = (
            'id',
            'profile',
            'created',
            'workout_day',
            'reps',
        )


class WorkoutLogView(ProfileAuthedAPIView):

    def put(self, request):
        """Create or patch workout log

        #### Query Parameters
        * default (or custom)
        * custom (or default)

        `?default` will delete default of given id.

        `?custom` will delete custom of given id.

        `default` takes precedence over `custom`.

        #### Body Parameters
        * reps: string -- comma separated string, eg. "5,5,5,4,3"
        * workout_day: integer

        #### Sample Response
        ```
        {
            "id": 1,
            "profile": 1,
            "workout_day": 1,
            "reps": "1,14"
        }
        ```
        """
        query_switches = get_query_switches(
            request.query_params,
            ['default', 'custom'],
            raise_on_none=True,
        )

        workout_log = None

        if request.data:
            if 'workout_day' not in request.data:
                return Response(
                    {'workout_day': ['This field is required.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                if 'default' in query_switches:
                    workout_day = WorkoutDay.objects.get(
                        pk=request.data['workout_day'],
                    )
                else:
                    workout_day = CustomWorkoutDay.objects.get(
                        pk=request.data['workout_day'],
                    )
                    if workout_day.workout_program.profile != request.profile:
                        return Response(
                            {'workout_day': [
                                'Workout day does not belong to you.',
                            ]},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            except (WorkoutDay.DoesNotExist, CustomWorkoutDay.DoesNotExist):
                return Response(
                    {'workout_day': ['Workout day does not exist.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            request.data._mutable = True
            request.data['profile'] = request.profile.pk
            request.data._mutable = False

            try:
                if 'default' in query_switches:
                    workout_log = WorkoutLog.objects.get(
                        profile=request.profile,
                        workout_day=workout_day,
                    )
                else:
                    workout_log = CustomWorkoutLog.objects.get(
                        profile=request.profile,
                        workout_day=workout_day,
                    )
            except (WorkoutLog.DoesNotExist, CustomWorkoutLog.DoesNotExist):
                pass

        if 'default' in query_switches:
            Serializer = WorkoutLogSerializer
        else:
            Serializer = CustomWorkoutLogSerializer

        serializer = Serializer(workout_log, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        errors = dict(serializer.errors)
        errors.pop('profile', None)

        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

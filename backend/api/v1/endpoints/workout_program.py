from api.views import ProfileAuthedAPIView
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.workout_day import WorkoutDay
from db_models.models.workout_program import WorkoutProgram
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class WorkoutProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutProgram
        fields = (
            'id',
            'name',
            'length',
        )


class WorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutDay
        fields = (
            'exercise',
            'exercise_name',
            'day_of_week_name',
            'sets',
            'reps',
            'weights',
        )


class WorkoutProgramsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of workout programs

        #### Query Parameters
        * default: 1 (optional)
        * custom: 1 (optional)

        No query parameters will return nothing.

        `?default=1` will return all default programs.

        `?custom=1` will return all custom programs available to the user.

        `?default=1&custom=1` will return both types.


        #### Sample Response
        ```
        {
            "default": [
                {
                    "id": 1,
                    "name": "StrongLifts 5x5",
                    "length": 30
                }
            ],
            "custom": [
                {
                    "id": 1,
                    "name": "Gary's Custom",
                    "length": 15
                }
            ]
        }
        ```
        """
        response_dict = {}

        if request.query_params.get('default') == '1':
            response_dict['default'] = WorkoutProgramSerializer(
                WorkoutProgram.objects.all(),
                many=True,
            ).data

        if request.query_params.get('custom') == '1':
            response_dict['custom'] = WorkoutProgramSerializer(
                request.profile.customworkoutprogram_set.all(),
                many=True,
            ).data

        return Response(response_dict)


class WorkoutProgramView(ProfileAuthedAPIView):

    def get(self, request, pk):
        """Get a specific workout program's details

        #### Query Parameters
        * default: 1 (or custom)
        * custom: 1 (or default)

        No query parameters will return 400.

        `?default=1` will return a default program of given id.

        `?custom=1` will return a custom program of given id, if
        available to the user; 404 otherwise.

        `default` takes precedence over `custom`.


        #### Sample Response
        ```
        {
            "program": {
                "id": 1,
                "name": "StrongLifts 5x5",
                "length": 30
            },
            "days": {
                "1": [
                    {
                        "exercise": 0,
                        "exercise_name": "Squat",
                        "day_of_week_name": "Monday",
                        "sets": 5,
                        "reps": "5,5,5,5,5",
                        "weights": "45,45,45,45,45"
                    },
                    {
                        "exercise": 1,
                        "exercise_name": "Bench Press",
                        "day_of_week_name": "Monday",
                        "sets": 5,
                        "reps": "5,5,5,5,5",
                        "weights": "45,45,45,45,45"
                    }
                ],
                "2": [
                    ...
                ],
                ...
            }
        }
        ```
        """
        if request.query_params.get('default') == '1':
            program = get_object_or_404(WorkoutProgram, pk=pk)
            days = program.workoutday_set.all()
        elif request.query_params.get('custom') == '1':
            program = get_object_or_404(CustomWorkoutProgram, pk=pk)
            if program.profile != request.profile:
                raise Http404()
            days = program.customworkoutday_set.all()
        else:
            return Response(
                {
                    'detail': 'One of `default` or `custom` '
                    + 'query parameter is required',
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        days_dict = {}
        for day in days:
            if day.day in days_dict:
                days_dict[day.day].append(day)
            else:
                days_dict[day.day] = [day]

        for day, day_list in days_dict.items():
            days_dict[day] = WorkoutDaySerializer(day_list, many=True).data

        return Response({
            'program': WorkoutProgramSerializer(program).data,
            'days': days_dict,
        })

    def post(self, request):
        pass

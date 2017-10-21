import simplejson as json
from api.v1.endpoints.workout_day import CustomWorkoutDaySerializer
from api.v1.endpoints.workout_day import WorkoutDaySerializer
from api.views import ProfileAuthedAPIView
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.workout_program import WorkoutProgram
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response


class StrintException(Exception):
    pass


class SerializerException(Exception):
    pass


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

    def post(self, request):
        """Create a custom workout program

        #### Body Parameters
        * name: string
        * days: json string (optional)

        ##### Days format
        ```
        {
            "1":[
                {
                    "exercise":0,
                    "day_of_week":1,
                    "reps":"5,5,5,5,5",
                    "weights":"45,45,45,45,45"
                },
                ...
            ],
            ...
        }
        ```

        #### Sample Response
        ```
        {
            "program": {
                "id": 11,
                "name": "Super",
                "length": 10
            },
            "days": {
                "1": [
                    {
                        "exercise": 0,
                        "day_of_week": 1,
                        "sets": 5,
                        "reps": "5,5,5,5,5",
                        "weights": "45,45,45,45,45"
                    },
                    ...
                ],
                ...
            }
        }
        ```
        """
        if not (
            request.data
            and request.data.get('name')
            and isinstance(request.data['name'], str)
        ):
            return Response(
                {'name': 'Must be a non-empty string.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            CustomWorkoutProgram.objects.get(
                profile=request.profile,
                name=request.data['name'],
            )
            return Response(
                {'name': 'Name already in use.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CustomWorkoutProgram.DoesNotExist:
            pass

        errors = {}
        try:
            with transaction.atomic():
                program = CustomWorkoutProgram.objects.create(
                    profile=request.profile,
                    name=request.data['name'],
                    length=0,
                )
                days = request.data.get('days')
                if days:
                    try:
                        days = json.loads(days)
                    except json.scanner.JSONDecodeError:
                        errors['days'] = 'Invalid JSON.'
                        raise
                    for day, exercises in days.items():
                        try:
                            day = int(day)
                        except ValueError:
                            errors['days'] = f'"{day}" is not an integer.'
                            raise StrintException()
                        for exercise in exercises:
                            exercise['workout_program'] = program.pk
                            exercise['day'] = day

                    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
                    days = [
                        item for sublist in list(
                            days.values(),
                        ) for item in sublist
                    ]

                    serializer = CustomWorkoutDaySerializer(
                        data=days,
                        many=True,
                    )

                    if serializer.is_valid():
                        serializer.save()
                        program.length = len(days)
                        program.full_clean()
                        program.save()
                    else:
                        errors['days'] = serializer.errors
                        raise SerializerException()
        except (
            json.scanner.JSONDecodeError,
            StrintException,
            SerializerException,
        ):
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            WorkoutProgramView.get_workout_program(
                program,
                program.customworkoutday_set.all(),
            ), status=status.HTTP_201_CREATED,
        )


class WorkoutProgramView(ProfileAuthedAPIView):

    @staticmethod
    def get_workout_program(program, days):
        days_dict = {}
        for day in days:
            if day.day in days_dict:
                days_dict[day.day].append(day)
            else:
                days_dict[day.day] = [day]

        for day, day_list in days_dict.items():
            days_dict[day] = WorkoutDaySerializer(day_list, many=True).data

        return {
            'program': WorkoutProgramSerializer(program).data,
            'days': days_dict,
        }

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
                        "day_of_week": 1,
                        "sets": 5,
                        "reps": "5,5,5,5,5",
                        "weights": "45,45,45,45,45"
                    },
                    {
                        "exercise": 1,
                        "day_of_week": 1,
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

        return Response(
            WorkoutProgramView.get_workout_program(
                program,
                days,
            ),
        )

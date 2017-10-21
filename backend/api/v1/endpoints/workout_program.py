import simplejson as json
from api.v1.endpoints.workout_day import CustomWorkoutDaySerializer
from api.v1.endpoints.workout_day import WorkoutDaySerializer
from api.views import ProfileAuthedAPIView
from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.custom_workout_day import CustomWorkoutDayException
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.workout_program import WorkoutProgram
from django.db import transaction
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


def _process_days_string(program, days_string):
    try:
        days = json.loads(days_string)
    except json.scanner.JSONDecodeError:
        raise CustomWorkoutDayException('Invalid JSON.')
    for day, exercises in days.items():
        try:
            day = int(day)
        except ValueError:
            raise CustomWorkoutDayException(f'"{day}" is not an integer.')
        for exercise in exercises:
            exercise['workout_program'] = program.pk
            exercise['day'] = day

    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    return [
        item for sublist in list(
            days.values(),
        ) for item in sublist
    ]


class WorkoutProgramsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of workout programs

        #### Query Parameters
        * default: 1 (optional)
        * custom: 1 (optional)

        No query parameters will return nothing.

        `?default` will return all default programs.

        `?custom` will return all custom programs available to the user.

        `?default&custom` will return both types.


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

        if 'default' in request.query_params:
            response_dict['default'] = WorkoutProgramSerializer(
                WorkoutProgram.objects.all(),
                many=True,
            ).data

        if 'custom' in request.query_params:
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

        try:
            with transaction.atomic():
                program = CustomWorkoutProgram.objects.create(
                    profile=request.profile,
                    name=request.data['name'],
                    length=0,
                )
                days_string = request.data.get('days')
                if days_string:
                    days = _process_days_string(program, days_string)

                    serializer = CustomWorkoutDaySerializer(
                        data=days,
                        many=True,
                    )

                    if serializer.is_valid():
                        serializer.save()
                        program.length = len(days)
                        program.save()
                    else:
                        raise CustomWorkoutDayException(serializer.errors)
        except CustomWorkoutDayException as e:
            return Response(
                {'days': e.errors}, status=status.HTTP_400_BAD_REQUEST,
            )

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
        * default (or custom)
        * custom (or default)

        No query parameters will return 400.

        `?default` will return a default program of given id.

        `?custom` will return a custom program of given id, if
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
        if 'default' in request.query_params:
            program = get_object_or_404(WorkoutProgram, pk=pk)
            days = program.workoutday_set.all()
        elif 'custom' in request.query_params:
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

    def patch(self, request, pk):
        """Update a custom workout program

        #### Body Parameters
        * name: string (optional)
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
                {
                    "exercise":3,
                    "delete":true
                },
                ...
            ],
            ...
        }
        ```

        Delete a day's exercise with `"delete":true`

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
        program = get_object_or_404(CustomWorkoutProgram, pk=pk)
        if program.profile != request.profile:
            raise Http404()

        if request.data:
            name = request.data.get('name')
            if name is not None and name != program.name:
                if not (name and isinstance(name, str)):
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
                program.name = name
                program.save()

            days_string = request.data.get('days')
            if days_string:
                try:
                    days = _process_days_string(program, days_string)
                    with transaction.atomic():
                        for day_data in days:
                            try:
                                # TODO: Slow.
                                day_set = program.customworkoutday_set
                                existing_day = day_set.get(
                                    day=day_data['day'],
                                    exercise=day_data['exercise'],
                                )
                            except CustomWorkoutDay.DoesNotExist:
                                existing_day = None

                            if day_data.get('delete') is True:
                                if existing_day:
                                    existing_day.delete()
                                    continue
                            else:
                                serializer = CustomWorkoutDaySerializer(
                                    existing_day,
                                    data=day_data,
                                )

                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    raise CustomWorkoutDayException(
                                        serializer.errors,
                                    )
                except CustomWorkoutDayException as e:
                    return Response(
                        {'days': e.errors}, status=status.HTTP_400_BAD_REQUEST,
                    )

        return Response(
            WorkoutProgramView.get_workout_program(
                program,
                program.customworkoutday_set.all(),
            ),
        )

    def delete(self, request, pk):
        """Delete a custom workout program
        """
        program = get_object_or_404(CustomWorkoutProgram, pk=pk)
        if program.profile != request.profile:
            raise Http404()

        program.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

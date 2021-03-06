import simplejson as json
from api.v1.endpoints.workout_day import CustomWorkoutDaySerializer
from api.v1.endpoints.workout_day import WorkoutDaySerializer
from api.views import ProfileAuthedAPIView
from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.custom_workout_day import CustomWorkoutDayException
from db_models.models.custom_workout_log import CustomWorkoutLog
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.workout_log import WorkoutLog
from db_models.models.workout_program import WorkoutProgram
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from utils.models import get_model_for_profile
from utils.query import get_query_switches


class WorkoutProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutProgram
        fields = (
            'id',
            'name',
            'length',
            'description',
        )


def _process_days_string(program, days_string):
    try:
        workout_days = json.loads(days_string)
    except json.scanner.JSONDecodeError:
        raise CustomWorkoutDayException('Invalid JSON.')

    for workout_day in workout_days:
        workout_day['workout_program'] = program.pk

    return workout_days


class WorkoutProgramsView(ProfileAuthedAPIView):

    def get(self, request):
        """Get a list of workout programs

        #### Query Parameters
        * default (optional)
        * custom (optional)

        `?default` will return all default programs.

        `?custom` will return all custom programs available to the user.

        You can `&` parameters together.
        No parameters is same as having all parameters.

        #### Sample Response
        ```
        {
            "default": [
                {
                    "id": 1,
                    "name": "StrongLifts 5x5",
                    "length": 30,
                    "description": "Hello."
                }
            ],
            "custom": [
                {
                    "id": 1,
                    "name": "Gary's Custom",
                    "length": 15,
                    "description": "World."
                }
            ]
        }
        ```
        """
        response_dict = {}

        query_switches = get_query_switches(
            request.query_params,
            ['default', 'custom'],
            all_true_on_none=True,
        )

        if 'default' in query_switches:
            response_dict['default'] = WorkoutProgramSerializer(
                WorkoutProgram.objects.all(),
                many=True,
            ).data

        if 'custom' in query_switches:
            response_dict['custom'] = WorkoutProgramSerializer(
                request.profile.customworkoutprogram_set.all(),
                many=True,
            ).data

        return Response(response_dict)

    def post(self, request):
        """Create a custom workout program

        #### Body Parameters
        * name: string
        * description: string (optional)
        * days: json string (optional)

        ##### Days format
        ```
        [
            {
                "week": 1,
                "day": 1,
                "exercise": 0,
                "sets": 5,
                "reps": 5,
                "weight": 45
            },
            ...
        ]
        ```

        #### Sample Response
        ```
        {
            "program": {
                "id": 1,
                "name": "StrongLifts 5x5",
                "length": 30,
                "description": "Hello"
            },
            "weeks": {
                "1": {
                    "1": [
                        {
                            "id": 0,
                            "exercise": 0,
                            "sets": 5,
                            "reps": 5,
                            "weight": 45,
                        },
                        ...
                    ],
                    ...
                },
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
            with transaction.atomic():
                program = CustomWorkoutProgram.objects.create(
                    profile=request.profile,
                    name=request.data['name'],
                    length=0,
                    description=request.data.get('description') or '',
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
    def get_workout_program(program, workout_days, profile=None, default=None):
        weeks = {}

        for workout_day in workout_days:
            if workout_day.week not in weeks:
                weeks[workout_day.week] = {}

            if workout_day.day not in weeks[workout_day.week]:
                weeks[workout_day.week][workout_day.day] = []

            weeks[workout_day.week][workout_day.day].append(
                WorkoutDaySerializer(workout_day).data,
            )

        if profile:
            for week in weeks.values():
                for days in week.values():
                    for i, day in enumerate(days):
                        day['log'] = None

                        try:
                            if default:
                                day['log'] = WorkoutLog.objects.get(
                                    profile=profile,
                                    workout_day=day['id'],
                                ).reps
                            else:
                                day['log'] = CustomWorkoutLog.objects.get(
                                    profile=profile,
                                    workout_day=day['id'],
                                ).reps
                        except (
                            WorkoutLog.DoesNotExist,
                            CustomWorkoutLog.DoesNotExist,
                        ):
                            pass

                        days[i] = day

        return {
            'program': WorkoutProgramSerializer(program).data,
            'weeks': weeks,
        }

    def get(self, request, pk):
        """Get a specific workout program's details

        #### Query Parameters
        * default (or custom)
        * custom (or default)

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
                "length": 30,
                "description": "Hello"
            },
            "weeks": {
                "1": {
                    "1": [
                        {
                            "id": 0,
                            "exercise": 0,
                            "sets": 5,
                            "reps": 5,
                            "weight": 45,
                            "log": "5,5,5,4,3"
                        },
                        {
                            "id": 1,
                            "exercise": 1,
                            "sets": 5,
                            "reps": 5,
                            "weight": 45,
                            "log": null
                        },
                        ...
                    ],
                    ...
                },
                ...
            }
        }
        ```
        """
        query_switches = get_query_switches(
            request.query_params,
            ['default', 'custom'],
            raise_on_none=True,
        )

        if 'default' in query_switches:
            program = get_object_or_404(WorkoutProgram, pk=pk)
            days = program.workoutday_set.all()
        else:
            program = get_model_for_profile(
                CustomWorkoutProgram,
                request.profile,
                pk=pk,
            )
            days = program.customworkoutday_set.all()

        return Response(
            WorkoutProgramView.get_workout_program(
                program,
                days,
                profile=request.profile,
                default=('default' in query_switches),
            ),
        )

    def patch(self, request, pk):
        """Update a custom workout program

        #### Body Parameters
        * name: string (optional)
        * description: string (optional)
        * days: json string (optional)

        ##### Days format

        ```
        [
            {
                "week": 1,
                "day": 1,
                "exercise": 0,
                "sets": 5,
                "reps": 5,
                "weight": 45
            },
            {
                "week": 1,
                "day": 2,
                "exercise" 0,
                "delete": true
            },
            ...
        ]
        ```

        Delete a day's exercise with `"delete":true`

        #### Sample Response
        ```
        {
            "program": {
                "id": 4,
                "name": "asd",
                "length": 2,
                "description": ""
            },
            "weeks": {
                "1": {
                    "1": [
                        {
                            "id": 4,
                            "exercise": 0,
                            "sets": 56,
                            "reps": 5,
                            "weight": 45,
                            "log": null
                        }
                    ]
                }
            }
        }
        ```
        """
        program = get_model_for_profile(
            CustomWorkoutProgram,
            request.profile,
            pk=pk,
        )

        if request.data:
            name = request.data.get('name')
            if name is not None and name != program.name:
                if not (name and isinstance(name, str)):
                    return Response(
                        {'name': 'Must be a non-empty string.'},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                program.name = name
            if 'description' in request.data:
                program.description = request.data['description'] or ''
            program.full_clean()
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
                                    week=day_data['week'],
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
                profile=request.profile,
                default=False,
            ),
        )

    def delete(self, request, pk):
        """Delete a custom workout program
        """
        program = get_model_for_profile(
            CustomWorkoutProgram,
            request.profile,
            pk=pk,
        )

        program.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

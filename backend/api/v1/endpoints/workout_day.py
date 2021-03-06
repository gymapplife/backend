from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.workout_day import WorkoutDay
from rest_framework import serializers


class WorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutDay
        fields = (
            'id',
            'exercise',
            'sets',
            'reps',
            'weight',
        )


class CustomWorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomWorkoutDay
        fields = (
            'id',
            'workout_program',
            'exercise',
            'week',
            'day',
            'sets',
            'reps',
            'weight',
        )

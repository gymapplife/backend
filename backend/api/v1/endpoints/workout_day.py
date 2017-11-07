from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.workout_day import WorkoutDay
from rest_framework import serializers


class WorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutDay
        fields = (
            'exercise',
            'day_of_week',
            'sets',
            'reps',
            'weight',
        )


class CustomWorkoutDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomWorkoutDay
        fields = (
            'workout_program',
            'day',
            'exercise',
            'day_of_week',
            'sets',
            'reps',
            'weight',
        )

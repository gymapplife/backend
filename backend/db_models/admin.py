from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.default_workout_program import DefaultWorkoutProgram
from db_models.models.exercise import Exercise
from db_models.models.profile import Profile
from db_models.models.workout_day import WorkoutDay
from db_models.models.workout_program import WorkoutProgram
from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('goal', 'experience', 'weight', 'height')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')


@admin.register(DefaultWorkoutProgram)
class DefaultWorkoutProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'length')


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = (
        'workout_program',
        'exercise',
        'day',
        'sets',
        'reps',
        'weights',
    )


@admin.register(CustomWorkoutDay)
class CustomWorkoutDayAdmin(admin.ModelAdmin):
    list_display = (
        'workout_day',
        'profile',
        'exercise',
        'day',
        'sets',
        'reps',
        'weights',
    )

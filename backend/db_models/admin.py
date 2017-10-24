from db_models.models.custom_workout_day import CustomWorkoutDay
from db_models.models.custom_workout_program import CustomWorkoutProgram
from db_models.models.day_of_week import DayOfWeek
from db_models.models.exercise import Exercise
from db_models.models.profile import Profile
from db_models.models.public_photo import PublicPhoto
from db_models.models.public_video import PublicVideo
from db_models.models.uploaded_photo import UploadedPhoto
from db_models.models.uploaded_video import UploadedVideo
from db_models.models.workout_day import WorkoutDay
from db_models.models.workout_program import WorkoutProgram
from django.contrib import admin


@admin.register(DayOfWeek)
class DayOfWeekAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'goal',
        'experience',
        'weight',
        'height',
    )


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):

    list_display = ('name', 'primary_muscle', 'photo', 'video')


@admin.register(WorkoutProgram)
class WorkoutProgramAdmin(admin.ModelAdmin):

    list_display = ('name', 'length')


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):

    list_display = (
        'workout_program',
        'exercise',
        'day',
        'day_of_week',
        'sets',
        'reps',
        'weights',
    )


@admin.register(CustomWorkoutProgram)
class CustomWorkoutProgramAdmin(admin.ModelAdmin):

    list_display = ('profile', 'name', 'length')


@admin.register(CustomWorkoutDay)
class CustomWorkoutDayAdmin(admin.ModelAdmin):

    list_display = (
        'workout_program',
        'exercise',
        'day',
        'day_of_week',
        'sets',
        'reps',
        'weights',
    )


@admin.register(PublicPhoto)
class PublicPhotoAdmin(admin.ModelAdmin):

    list_display = ('name', 'download_url')


@admin.register(PublicVideo)
class PublicVideoAdmin(admin.ModelAdmin):

    list_display = ('name', 'download_url')


@admin.register(UploadedPhoto)
class UploadedPhotoAdmin(admin.ModelAdmin):

    list_display = ('name', 'download_url')


@admin.register(UploadedVideo)
class UploadedVideoAdmin(admin.ModelAdmin):

    list_display = ('name', 'download_url')

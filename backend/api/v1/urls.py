from api.v1.endpoints.exercise import ExercisesView
from api.v1.endpoints.exercise import ExerciseView
from api.v1.endpoints.media import MediasView
from api.v1.endpoints.media import MediaView
from api.v1.endpoints.profile import ProfileView
from api.v1.endpoints.workout_log import WorkoutLogView
from api.v1.endpoints.workout_program import WorkoutProgramsView
from api.v1.endpoints.workout_program import WorkoutProgramView
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='API Documentation')


urlpatterns = [
    url('^$', schema_view),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(
        r'^workout-programs/$', WorkoutProgramsView.as_view(),
        name='workout_programs',
    ),
    url(
        r'^workout-programs/(?P<pk>[0-9]+)/$', WorkoutProgramView.as_view(),
        name='workout_program',
    ),
    url(
        r'^media/$', MediasView.as_view(),
        name='medias',
    ),
    url(
        r'^media/(?P<pk>[0-9]+)/$', MediaView.as_view(),
        name='media',
    ),
    url(
        r'^exercise/$', ExercisesView.as_view(),
        name='exercises',
    ),
    url(
        r'^exercise/(?P<pk>[0-9]+)/$', ExerciseView.as_view(),
        name='exercise',
    ),
    url(
        r'^workout-log/$', WorkoutLogView.as_view(),
        name='workout_log',
    ),
]

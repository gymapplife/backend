from api.v1.endpoints.profile import ProfileView
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    url('^$', schema_view),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

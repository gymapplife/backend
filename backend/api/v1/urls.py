from api.v1.endpoints.profile import ProfileView
from django.conf.urls import url

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

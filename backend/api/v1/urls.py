from api.v1.views.profile import ProfileView
from django.conf.urls import url

urlpatterns = [
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
]

from api.v1 import views
from django.conf.urls import url

urlpatterns = [
    url(r'^profile/$', views.Profile.as_view(), name='profile'),
]

from django.conf.urls import include
from django.conf.urls import url


urlpatterns = [
    url(r'^v1/', include('api.v1.urls')),
]

from django.http import HttpResponse

from backend.settings import BASIC_AUTH_REALM


def HttpResponseUnauthorized(*args, **kwargs):
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = f'Basic realm="{BASIC_AUTH_REALM}"'
    return response

from django.http import HttpResponse
from django.http import HttpResponseBadRequest

from backend.settings import BASIC_AUTH_REALM


def unauthorized_response():
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = f'Basic realm="{BASIC_AUTH_REALM}"'
    return response


def missing_param_response(param):
    return HttpResponseBadRequest(f'Missing parameter: {param}')

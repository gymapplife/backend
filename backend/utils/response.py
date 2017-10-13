from django.http import HttpResponse
from django.http import HttpResponseForbidden

from backend.settings import BASIC_AUTH_REALM


def HttpResponseUnauthorized():
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = f'Basic realm="{BASIC_AUTH_REALM}"'
    return response


def NoProfileForbiddenResponse():
    return HttpResponseForbidden(
        'No GymApp.life profile exists for given Facebook account.',
    )

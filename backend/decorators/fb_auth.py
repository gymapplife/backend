import base64

from db_models.models.profile import Profile
from lib.fb_token import fb_token_is_valid
from rest_framework import status
from rest_framework.response import Response
from utils.response import HttpResponseUnauthorized

# from backend.settings import DEBUG


def _request_with_fb_auth_or_none(request):
    """Returns request with fb_id and fb_token populated
    or None if bad auth

    Inspired by:
    https://gist.github.com/codeinthehole/4732233
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            uid, token = base64.b64decode(
                auth[1],
            ).decode('utf-8').split(':')
            if fb_token_is_valid(uid, token):  # or DEBUG:
                request.fb_id = uid
                request.fb_token = token
                return request
    return None


def fb_auth_required(view):
    """View method decorator

    Adds profile to request
    Returns 401 if invalid auth
    Returns 403 if no profile associated with fb_id

    Inspired by:
    https://simpleisbetterthancomplex.com/2015/12/07/working-with-django-view-decorators.html
    """
    def wrap(request, *args, **kwargs):
        request = _request_with_fb_auth_or_none(request)
        if request:
            try:
                request.profile = Profile.objects.get(id=request.fb_id)
            except:
                return Response(status=status.HTTP_403_FORBIDDEN)
            return view(request, *args, **kwargs)
        return HttpResponseUnauthorized()
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def fb_auth_required_no_profile(view):
    """Same as fb_auth_required, but doesn't attach a profile to the request
    Made specifically for creating profiles
    """
    def wrap(request, *args, **kwargs):
        request = _request_with_fb_auth_or_none(request)
        if request:
            return view(request, *args, **kwargs)
        return HttpResponseUnauthorized()
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap

import base64

from db_models.models.profile import Profile
from lib.fb_token import fb_token_is_valid
from utils.response import unauthorized_response

from backend.settings import DEBUG


def _basic_auth_is_valid(request):
    """Returns False, for bad auth; or request with fb_id and fb_token populated

    Inspired by:
    https://gist.github.com/codeinthehole/4732233
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2 and auth[0].lower() == 'basic':
            uid, token = base64.b64decode(
                auth[1],
            ).decode('utf-8').split(':')
            if fb_token_is_valid(uid, token) or DEBUG:
                request.fb_id = uid
                request.fb_token = token
                return request
    return False


def fb_auth_required(view):
    """View method decorator

    Inspired by:
    https://simpleisbetterthancomplex.com/2015/12/07/working-with-django-view-decorators.html
    """
    def wrap(request, *args, **kwargs):
        request = _basic_auth_is_valid(request)
        if request:
            try:
                profile = Profile.objects.get(id=request.fb_id)
            except:
                return unauthorized_response()
            request.profile = profile
            request.user = profile.user
            return view(request, *args, **kwargs)
        return unauthorized_response()
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap


def fb_auth_required_no_profile(view):
    """Same as fb_auth_required, but doesn't attach a profile to the request
    Made specifically for creating profiles
    """
    def wrap(request, *args, **kwargs):
        request = _basic_auth_is_valid(request)
        if request:
            return view(request, *args, **kwargs)
        return unauthorized_response()
    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap

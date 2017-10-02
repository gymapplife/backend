import base64

from db_models.models.profile import Profile
from django.http import HttpResponse
from lib.fb_token import fb_token_is_valid

from backend.settings import BASIC_AUTH_REALM


def fb_auth_required(view):
    """View method decorator

    Inspired by:
    https://gist.github.com/codeinthehole/4732233
    https://simpleisbetterthancomplex.com/2015/12/07/working-with-django-view-decorators.html
    """
    def wrap(request, *args, **kwargs):

        def unauthorized_response():
            response = HttpResponse()
            response.status_code = 401
            response['WWW-Authenticate'] = f'Basic realm="{BASIC_AUTH_REALM}"'
            return response

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    uid, token = base64.b64decode(
                        auth[1],
                    ).decode('utf-8').split(':')
                    if fb_token_is_valid(uid, token):
                        try:
                            profile = Profile.objects.get(id=uid)
                        except:
                            return unauthorized_response()
                        request.profile = profile
                        request.user = profile.user
                        return view(request, *args, **kwargs)

        return unauthorized_response()

    wrap.__doc__ = view.__doc__
    wrap.__name__ = view.__name__
    return wrap

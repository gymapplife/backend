import base64
import logging

from lib.facebook_auth import facebook_auth_error
from utils.response import HttpResponseUnauthorized

from backend.settings import DEBUG


logger = logging.getLogger(__name__)


class FacebookAuthMixin:

    def dispatch(self, request, *args, **kwargs):
        """View mixin for Basic auth -- facebook_id:facebook_token

        request object will be populated with:
            request.fb_id
            request.fb_token

        Inspired by:
        https://gist.github.com/codeinthehole/4732233
        """
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()

            if len(auth) == 2 and auth[0].lower() == 'basic':
                fb_id, fb_token = base64.b64decode(
                    auth[1],
                ).decode('utf-8').split(':')

                auth_error = facebook_auth_error(fb_id, fb_token)

                if DEBUG and auth_error:
                    logger.warning('Not returning 401 because DEBUG=True')
                    logger.warning(auth_error)

                if not auth_error or DEBUG:
                    request.fb_id = fb_id
                    request.fb_token = fb_token

                    return super().dispatch(
                        request,
                        *args,
                        **kwargs,
                    )

        return HttpResponseUnauthorized()

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from mixins.facebook_auth_mixin import FacebookAuthMixin
from mixins.profile_mixin import ProfileMixin
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AuthedAPIView(FacebookAuthMixin, APIView):

    pass


@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileAuthedAPIView(FacebookAuthMixin, ProfileMixin, APIView):

    pass

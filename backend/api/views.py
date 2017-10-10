from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from mixins.facebook_auth_mixin import FacebookAuthMixin
from rest_framework.views import APIView


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AuthedAPIView(FacebookAuthMixin, APIView):
    pass

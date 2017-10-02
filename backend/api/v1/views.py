from decorators.fb_auth import fb_auth_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie


@method_decorator(fb_auth_required, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class Profile(View):
    def get(self, request):
        """Get profile info
        """
        return JsonResponse({
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'goal': request.profile.goal,
            'experience': request.profile.experience,
            'weight': request.profile.weight,
            'height': request.profile.height,
            'age': request.profile.age,
        })

    def post(self, request):
        """Create a profile
        """
        return JsonResponse({})

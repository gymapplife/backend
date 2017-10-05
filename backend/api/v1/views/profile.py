from db_models.models.profile import Profile
from decorators.fb_auth import fb_auth_required_no_profile
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from utils.response import missing_param_response
from utils.response import unauthorized_response


@method_decorator(fb_auth_required_no_profile, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class ProfileView(View):
    def get(self, request):
        """Get profile
        """
        try:
            profile = Profile.objects.get(id=request.fb_id)
        except:
            return unauthorized_response()
        return JsonResponse({
            'goal': profile.goal,
            'experience': profile.experience,
            'weight': profile.weight,
            'height': profile.height,
        })

    def post(self, request):
        """Create a profile
        """
        try:
            goal = request.POST['goal']
            experience = request.POST['experience']
            weight = int(request.POST['weight'])
            height = int(request.POST['height'])
        except MultiValueDictKeyError as e:
            return missing_param_response(e.args[0])
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        try:
            Profile.objects.get(id=request.fb_id)
            return HttpResponseBadRequest(
                f"Facebook ID already in use: '{request.fb_id}'",
            )
        except:
            pass

        Profile.objects.create(
            id=request.fb_id,
            goal=goal,
            experience=experience,
            weight=weight,
            height=height,
        )

        json_response = JsonResponse({
            'goal': goal,
            'experience': experience,
            'weight': weight,
            'height': height,
        })
        json_response.status_code = 201
        return json_response

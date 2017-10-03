from db_models.models.profile import Profile
from decorators.fb_auth import fb_auth_required_no_profile
from django.contrib.auth.models import User
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
            'first_name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
            'goal': profile.goal,
            'experience': profile.experience,
            'weight': profile.weight,
            'height': profile.height,
            'age': profile.age,
        })

    def post(self, request):
        """Create a profile
        """
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            goal = request.POST['goal']
            experience = request.POST['experience']
            weight = int(request.POST['weight'])
            height = int(request.POST['height'])
            age = int(request.POST['age'])
        except MultiValueDictKeyError as e:
            return missing_param_response(e.args[0])
        except ValueError as e:
            return HttpResponseBadRequest(str(e))

        try:
            User.objects.get(username=email, email=email)
            return HttpResponseBadRequest(f"Email already in use: '{email}'")
        except:
            pass

        try:
            Profile.objects.get(id=request.fb_id)
            return HttpResponseBadRequest(
                f"Facebook ID already in use: '{request.fb_id}'",
            )
        except:
            pass

        user = User.objects.create(username=email, email=email)
        Profile.objects.create(
            id=request.fb_id,
            user=user,
            goal=goal,
            experience=experience,
            weight=weight,
            height=height,
            age=age,
        )

        json_response = JsonResponse({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'goal': goal,
            'experience': experience,
            'weight': weight,
            'height': height,
            'age': age,
        })
        json_response.status_code = 201
        return json_response

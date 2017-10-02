from django.http import JsonResponse
from django.views import View


class Profile(View):
    def get(self, request):
        return JsonResponse({})

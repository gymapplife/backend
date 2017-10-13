from db_models.models.profile import Profile
from utils.response import NoProfileForbiddenResponse


class ProfileMixin:

    def dispatch(self, request, *args, **kwargs):
        """View mixin for populating request.profile

        request.fb_id must be avaliable
        """
        try:
            request.profile = Profile.objects.get(id=request.fb_id)
        except:
            return NoProfileForbiddenResponse()

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )

from django.http import Http404
from django.shortcuts import get_object_or_404


def get_model_for_profile(Model, profile, **kwargs):
    model = get_object_or_404(Model, **kwargs)
    if model.profile != profile:
        raise Http404()
    return model

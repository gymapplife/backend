from db_models.models.profile import Profile
from db_models.validators import validate_comma_separated_ints
from django.db import models


class AbstractWorkoutLog(models.Model):

    class Meta:
        abstract = True

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

    # Comma separated string of how many reps the user did for each set
    # eg. 5,5,5,4,3
    # Idk why anyone would want 64 chars worth, but w.e
    reps = models.CharField(
        max_length=64,
        validators=[validate_comma_separated_ints],
    )

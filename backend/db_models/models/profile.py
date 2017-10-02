from django.contrib.auth.models import User
from django.db import models
from utils.namedtuple import namedtuple_and_choices_from_kwargs


class Profile(models.Model):

    Goal, _goal_choices = namedtuple_and_choices_from_kwargs(
        'Goal',
        STRENGTH_TRAINING='Strength Training',
        LOSE_WEIGHT='Lose Weight',
        CADRIO='Cardio',
    )

    Experience, _experience_choices = namedtuple_and_choices_from_kwargs(
        'Experience',
        NEW='New',
        LT_ONE='Less than 1 year',
        ONE_TO_THREE='1 to 3 years',
        GT_THREE='More than 3 years',
    )

    # This is their Facebook user id
    id = models.BigIntegerField(primary_key=True, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    goal = models.CharField(
        max_length=len(max(Goal._fields, key=len)),
        choices=_goal_choices,
    )

    experience = models.CharField(
        max_length=len(max(Experience._fields, key=len)),
        choices=_experience_choices,
    )

    weight = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    age = models.PositiveSmallIntegerField()

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        email = self.user.email
        return f'{first_name} {last_name} <{email}>'

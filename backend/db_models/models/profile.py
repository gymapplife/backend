from django.db import models
from utils.namedtuple import namedtuple_and_choices_from_kwargs


class Profile(models.Model):

    Goal, _goal_choices = namedtuple_and_choices_from_kwargs(
        'Goal',
        STRENGTH_TRAINING='Strength Training',
        LOSE_WEIGHT='Lose Weight',
        CARDIO='Cardio',
    )

    Experience, _experience_choices = namedtuple_and_choices_from_kwargs(
        'Experience',
        NEW='New',
        BEGINNER='Beginner',
        NOVICE='Novice',
        INTERMEDIATE='Intermediate',
        ADVANCED='Advanced',
    )

    # This is their Facebook user id
    id = models.BigIntegerField(primary_key=True, editable=False)

    goal = models.CharField(
        max_length=len(max(Goal._fields, key=len)),
        choices=_goal_choices,
    )

    experience = models.CharField(
        max_length=len(max(Experience._fields, key=len)),
        choices=_experience_choices,
    )

    # Body weight in kg
    weight = models.PositiveSmallIntegerField()

    # Height in cm
    height = models.PositiveSmallIntegerField()

from db_models.models.profile import Profile
from django.db import models
from utils.namedtuple import namedtuple_and_choices_from_kwargs


class FoodLog(models.Model):

    Meal, _meal_choices = namedtuple_and_choices_from_kwargs(
        'Meal',
        BREAKFAST='Breakfast',
        LUNCH='Lunch',
        DINNER='Dinner',
        SNACK='Snack',
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        db_index=True,
    )

    name = models.CharField(max_length=64)

    created = models.DateTimeField(auto_now_add=True)

    calories = models.PositiveSmallIntegerField()

    meal = models.CharField(
        max_length=len(max(Meal._fields, key=len)),
        choices=_meal_choices,
    )

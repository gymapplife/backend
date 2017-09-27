from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        email = self.user.email
        return f'{first_name} {last_name} <{email}>'

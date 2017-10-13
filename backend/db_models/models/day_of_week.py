from django.db import models


class DayOfWeek(models.Model):

    name = models.CharField(max_length=9)

    def __str__(self):
        return self.name

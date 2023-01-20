
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        max_length=39,
        null=False,
        blank=False,
        default=True,
    )

    last_name = models.CharField(
        max_length=39,
        null=False,
        blank=False,
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.username)



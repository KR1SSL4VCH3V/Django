from django.contrib.auth.models import User
from django.db import models

from to_do_app.accounts.models import AppUser


class Task(models.Model):
    MAX_LENGTH_CHAR = 50


    title = models.CharField(
        max_length=MAX_LENGTH_CHAR,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    complete = models.BooleanField(
        default=False,
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']

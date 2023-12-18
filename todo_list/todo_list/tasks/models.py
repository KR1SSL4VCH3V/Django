from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


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

    priority = models.BooleanField(
        default=False,
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
        ordering = ['priority']

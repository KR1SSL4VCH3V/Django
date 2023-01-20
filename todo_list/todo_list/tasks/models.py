
from django.contrib.auth.models import User
from django.db import models

UserModel = User


class Task(models.Model):
    MAX_LENGTH_CHAR = 50

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

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

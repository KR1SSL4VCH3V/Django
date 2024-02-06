from django.db import models
from django.utils.formats import date_format

from task_manager.accounts.models import CustomUser


class Task(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    title = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    priority = models.BooleanField(
        default=False,
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.title}. Created on {date_format(self.created_date, 'SHORT_DATE_FORMAT')}"

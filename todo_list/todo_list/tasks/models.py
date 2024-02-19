from django.utils import timezone
import datetime
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

    created_date = models.DateField(
        auto_now_add=True,
    )

    due_date = models.DateField(
        default=datetime.date.today,
    )

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return (f"{self.title}. Created on {date_format(self.created_date, 'SHORT_DATE_FORMAT')}."
                f" Due on {self.due_date}")

    def is_expired(self):
        return self.due_date < timezone.now() - datetime.timedelta(days=13)

    def save(self, *args, **kwargs):
        if self.created_date and not self.due_date:
            self.due_date = self.created_date + datetime.timedelta(days=14)
        super().save(*args, **kwargs)

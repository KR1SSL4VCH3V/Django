from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        null=False,
        blank=False,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    class Meta:
        app_label = 'accounts'

    groups = models.ManyToManyField(
        Group,
        related_name='custom_users',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users',
    )


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.user)

    def full_clean(self, exclude=None, validate_unique=True, validate_constraints=True):
        return super().full_clean()

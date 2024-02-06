from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.db import models
from django.db.models import Q

# Adding CustomUserManager to enable the user to register with a username or email.

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_users_groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_users_permissions',
    )

    #  Make the email field unique to avoid duplication.

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

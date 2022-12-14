from django.contrib.auth import models as auth_models
from django.core import validators
from django.db import models

from to_do_app.core.validators import validate_letters


class AppUser(auth_models.AbstractUser):
    MIN_FIRST_NAME_LENGTH = 2
    MAX_FIRST_NAME_LENGTH = 30
    MIN_LAST_NAME_LENGTH = 2
    MAX_LAST_NAME_LENGTH = 30
    # GENDER_CHOICES = (
    #     (0, 'Male'),
    #     (1, 'Female'),
    #     (2, 'Other'),
    #     (3, 'Decline to state'),
    # )

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            validators.MinLengthValidator(MIN_FIRST_NAME_LENGTH),
            validate_letters,
        ),
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            validators.MinLengthValidator(MIN_LAST_NAME_LENGTH),
            validate_letters,
        ),
        null=False,
        blank=False,
    )

    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    # gender = models.IntegerField(
    #     choices=GENDER_CHOICES,
    #     null=False,
    #     blank=False,
    # )



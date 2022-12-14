from django.core.exceptions import ValidationError


def validate_letters(value):
    for ch in value:
        if not ch.isalpha():
            raise ValidationError('The name must to consist at least one letter')
import re

from rest_framework import serializers

SPECIAL_CHARS = r"[!@#$%^&*(),.?\":{}|<>]"


def validate_password1(value):
    if len(value) < 8:
        raise serializers.ValidationError('The password must be at least 8 characters!')

    if not re.search(r"\d", value):
        raise serializers.ValidationError('The password must contain at least one digit!')

    if not re.search('[A-Z]', value):
        raise serializers.ValidationError('The password must contain at least one capital letter!')

    if not re.search(SPECIAL_CHARS, value):
        raise serializers.ValidationError('The password must contain at least one special character!')

    return value

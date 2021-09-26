from django.core.exceptions import ValidationError


def greater_then_zero(value):
    if value == 0:
        raise ValidationError(
            ("Укажите значение больше 0")
        )

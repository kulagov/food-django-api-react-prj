from django.core.exceptions import ValidationError


def validate_int_field(value):
    if value < 1:
        raise ValidationError(
            ('Значение должно быть не менее 1'),
            params={'value': value},
        )

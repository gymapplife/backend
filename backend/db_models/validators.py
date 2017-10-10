from django.core.exceptions import ValidationError


def validate_comma_separated_ints(string):
    for x in string.split(','):
        try:
            if len(str(int(x))) != len(x):
                raise Exception()
        except:
            raise ValidationError(
                'Must be a comma seperated list of ints, without any spaces.',
            )

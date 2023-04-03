fieldAllowed = {
    'boolean': 'BooleanField',
    'char': 'CharField',
    'integer': 'IntegerField',
    'positiveinteger': 'PositiveIntegerField',
    'text': 'TextField',
    'date': 'DateTimeField',
}


def generate_field(field_name: str, field_type: str) -> str:
    return f"{fieldAllowed[field_type.lower()]}()"

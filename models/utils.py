# HTK Imports
from htk.utils.datetime_utils import parse_datetime
from htk.utils.general import strtobool_safe


# isort: off


def normalize_model_field_value(model, field, value):
    """Deserializes/normalizes the value for a particular model field.

    `value` typically comes from the value of a particular `field` of a JSON payload
    from an API call.

    For example, if the `value` is `None`, but the `field` is `models.BooleanField`,
    apply `bool(value)`
    """
    internal_type = model._meta.get_field(field).get_internal_type()

    if internal_type == 'BooleanField':
        normalized_value = strtobool_safe(value)
    elif internal_type in ('DateField', 'DateTimeField'):
        normalized_value = parse_datetime(value) if value is not None else None
    else:
        normalized_value = value

    return normalized_value

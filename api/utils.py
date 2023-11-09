# Python Standard Library Imports
import datetime
import json
from decimal import Decimal
from time import mktime

# Third Party (PyPI) Imports
import rollbar

# Django Imports
from django.core import serializers
from django.http import (
    HttpResponse,
    QueryDict,
)

# HTK Imports
from htk.api.constants import *
from htk.models import HtkBaseModel


# isort: off


class HtkJSONEncoder(serializers.json.DjangoJSONEncoder):
    def default(self, obj):
        from django.contrib.auth import get_user_model

        UserModel = get_user_model()

        if isinstance(obj, datetime.datetime):
            value = int(mktime(obj.timetuple()))
        elif isinstance(obj, Decimal):
            # fallback to string if `should_quantize` is False
            from htk.utils import htk_setting

            should_quantize = htk_setting('HTK_JSON_DECIMAL_SHOULD_QUANTIZE')
            quantize = Decimal(htk_setting('HTK_JSON_DECIMAL_QUANTIZE'))
            value = (
                float(obj.quantize(quantize)) if should_quantize else str(obj)
            )
        elif isinstance(obj, HtkBaseModel):
            value = obj.json_encode()
        elif isinstance(obj, UserModel):
            user = obj
            value = user.profile.json_encode()
        elif hasattr(obj, 'json_encode'):
            value = obj.json_encode()
        else:
            try:
                value = super(HtkJSONEncoder, self).default(obj)
            except:
                rollbar.report_exc_info(
                    extra_data={
                        'obj': obj,
                    }
                )
                value = (
                    -3.14159
                )  # return an absurd value so that we know the object wasn't serializable
        return value


def to_json(obj, encoder=HtkJSONEncoder):
    if hasattr(obj, '_meta'):
        if hasattr(obj, '__contains__'):
            return serializers.serialize('json', obj)
        else:
            return serializers.serialize('json', [obj])
    else:
        return json.dumps(obj, cls=encoder)


def json_okay(data=None):
    if data is None:
        data = {}
    data.update(
        {
            HTK_API_JSON_KEY_SUCCESS: True,
            HTK_API_JSON_KEY_STATUS: HTK_API_JSON_VALUE_OKAY,
        }
    )
    return data


def json_error(data=None):
    if data is None:
        data = {}
    data.update(
        {
            HTK_API_JSON_KEY_SUCCESS: False,
            HTK_API_JSON_KEY_STATUS: HTK_API_JSON_VALUE_ERROR,
        }
    )
    return data


def json_okay_str():
    return to_json(json_okay())


def json_error_str():
    return to_json(json_error())


def json_response(obj, encoder=HtkJSONEncoder, status=200):
    # TODO: consider the new django.http.response.JsonResponse in Django 1.7
    # https://docs.djangoproject.com/en/1.7/ref/request-response/
    response = HttpResponse(
        to_json(obj, encoder=encoder),
        content_type='application/json',
        status=status,
    )
    return response


def json_response_okay(data=None):
    data = json_okay(data=data)
    response = json_response(data)
    return response


def json_response_error(data=None, status=400):
    data = json_error(data=data)
    response = json_response(data, status=status)
    return response


def json_response_not_found():
    response = json_response_error({'error': 'Not Found'}, status=404)
    return response


def json_response_forbidden():
    response = json_response_error({'error': 'Forbidden'}, status=403)
    return response


def json_response_form_error(form):
    """Helper function for returning Django form errors originating from an API call

    Returns a dictionary of field and non-field errors.

    Example:
    {
        'errors': {
            'form_fields': {
                'username': ['message': 'error message', ...],
                'password': ['message': 'error message', ...],
            },
            'non_fields': ['error message', ...],
        }
    }
    """
    payload = json_response_error(
        {
            'errors': {
                'form_fields': form.errors,
                'non_fields': form.non_field_errors(),
            },
        }
    )
    return payload


def extract_post_params(
    post_data, expected_params, list_params=None, strict=True
):
    """Extract `expected_params` from `post_data`

    Raise Exception if `strict` and any `expected_params` are missing
    """
    data = QueryDict(mutable=True)
    if list_params is None:
        list_params = []
    for param in expected_params:
        if strict and param not in post_data:
            raise Exception('Missing param: %s' % param)
        if param in list_params:
            value = post_data.getlist(
                '%s[]' % param, post_data.getlist(param, False)
            )
            if value is not False:
                value = json.dumps(value)
                data[param] = value
        else:
            value = post_data.get(param)
            if value is not None:
                data[param] = value
    return data

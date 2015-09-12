import datetime
import json
import rollbar
from time import mktime

from django.core import serializers
from django.http import HttpResponse

from htk.api.constants import *

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            value = int(mktime(obj.timetuple()))
        else:
            try:
                value = json.JSONEncoder.default(self, obj)
            except:
                rollbar.report_exc_info(extra_data={'obj': obj,})
                value = -3.14159 # return an absurd value so that we know the object wasn't serializable
        return value

def to_json(obj, encoder=CustomJSONEncoder):
    if hasattr(obj, '_meta'):
        if hasattr(obj, '__contains__'):
            return serializers.serialize('json', obj )
        else:
            return serializers.serialize('json', [ obj ])
    else:
        return json.dumps(obj, cls=encoder)

def json_okay():
    return { HTK_API_JSON_KEY_STATUS : HTK_API_JSON_VALUE_OKAY }

def json_error():
    return { HTK_API_JSON_KEY_STATUS : HTK_API_JSON_VALUE_ERROR }

def json_okay_str():
    return to_json(json_okay())

def json_error_str():
    return to_json(json_error())

def json_response(obj, encoder=CustomJSONEncoder):
    return HttpResponse(to_json(obj, encoder=encoder), content_type='application/json')

def json_response_okay():
    return json_response(json_okay())

def json_response_error():
    return json_response(json_error())

def extract_post_params(post_data, expected_params, strict=True):
    """Extract `expected_params` from `post_data`

    Raise Exception if `strict` and any `expected_params` are missing
    """
    data = {}
    for param in expected_params:
        if strict and param not in post_data:
            raise Exception('Missing param: %s' % param)
        value = post_data.get(param)
        data[param] = value
    return data

import datetime
import json

from django.core import serializers
from django.http import HttpResponse

from htk.api.constants import *

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

def to_json(obj):
    if hasattr(obj, '_meta'):
        if hasattr(obj, '__contains__'):
            return serializers.serialize('json', obj )
        else:
            return serializers.serialize('json', [ obj ])
    else:
        return json.dumps(obj, cls=MyEncoder)

def json_okay():
    return { HTK_API_JSON_KEY_STATUS : HTK_API_JSON_VALUE_OKAY }

def json_error():
    return { HTK_API_JSON_KEY_STATUS : HTK_API_JSON_VALUE_ERROR }

def json_okay_str():
    return to_json(json_okay())

def json_error_str():
    return to_json(json_error())

def json_response(obj):
    return HttpResponse(to_json(obj), mimetype='application/json')    

def json_response_okay():
    return json_response(json_okay())

def json_response_error():
    return json_response(json_error())

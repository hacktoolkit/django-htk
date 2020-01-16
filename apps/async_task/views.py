# Python Standard Library Imports
import base64
import json


def async_download_result(request, result_id, result_is_json=False, content_type='text/plain', filename=None):
    """View to download the result of an async task as a file

    If `result_is_json` is `True`, infer filename and content_type
    """
    from celery.result import AsyncResult
    result = AsyncResult(result_id)

    if request.GET.get('ping'):
        # only check if the file is ready
        from htk.api.utils import json_response
        response = json_response({
            'ready' : result.ready(),
        })
    else:
        # attempt to download file
        if result.ready():
            from django.http import HttpResponse
            result_data = result.get()
            if result_is_json:
                from htk.apps.async_task.utils import extract_async_task_result_json_values
                content, content_type, filename = extract_async_task_result_json_values(result_data)
            else:
                if filename is None:
                    from htk.apps.async_task.constants import CONTENT_TYPE_FILE_EXTENSIONS
                    file_extension = '.%s' % CONTENT_TYPE_FILE_EXTENSIONS.get(content_type, 'txt')
                    filename = 'result' % file_extension
                else:
                    pass

                content = result_data

            response = HttpResponse(content, content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        else:
            from htk.utils.http.response import HttpResponseAccepted
            response = HttpResponseAccepted()
    return response

def async_task_status(request, result_id):
    from celery.result import AsyncResult
    result = AsyncResult(result_id)

    # check if the task is ready
    from htk.api.utils import json_response
    response = json_response({
        # possible states: PENDING | STARTED | RETRY | FAILURE | SUCCESS
        # see celery/result.py
        'state' : result.state,
        'ready' : result.ready(),
    })
    return response

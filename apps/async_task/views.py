def async_download_result(request, result_id, content_type='text/plain', filename=None):
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
            response = HttpResponse(result.get(), content_type=content_type)
            if filename is None:
                from htk.apps.async_task.constants import CONTENT_TYPE_FILE_EXTENSIONS
                file_extension = '.%s' % CONTENT_TYPE_FILE_EXTENSIONS.get(content_type, 'txt')
                filename = 'result' % file_extension
            response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        else:
            from htk.utils.http.response import HttpResponseAccepted
            response = HttpResponseAccepted()
    return response

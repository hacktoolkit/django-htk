def async_download_result(request, result_id):
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
            response = HttpResponse(result.get(), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s"' % 'applicants_contact_data_export.csv'
        else:
            from htk.utils.http.response import HttpResponseAccepted
            response = HttpResponseAccepted()
    return response

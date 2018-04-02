from django.http import HttpResponse

class HttpResponseAccepted(HttpResponse):
    status_code = 202

from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.template import loader

from htk.view_helpers import render_to_response_custom as _r

def google_site_verification(request, code):
    template_name = 'google_site_verification/google%s.html' % code
    try:
        response = _r(template_name)
    except TemplateDoesNotExist:
        response = None
        raise Http404
    return response

def bing_site_auth(request):
    template = loader.get_template('BingSiteAuth.xml')
    context = RequestContext(request, {})
    response = HttpResponse(template.render(context), mimetype="text/xml")
    return response

def html_site_verification(request, code):
    template_name = 'html_site_verification/%s--.html' % code
    try:
        response = _r(template_name)
    except TemplateDoesNotExist:
        response = None
        raise Http404
    return response

def robots(request):
    template = loader.get_template('robots.txt')
    context = RequestContext(request, {})
    response = HttpResponse(template.render(context), mimetype="text/plain")
    return response

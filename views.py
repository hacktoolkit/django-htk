from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import RequestContext
from django.template import TemplateDoesNotExist
from django.template import loader

def generic_template_view(request, template_name, mimetype='text/html'):
    try:
        template = loader.get_template(template_name)
        context = RequestContext(request, {})
        response = HttpResponse(template.render(context), mimetype=mimetype)
    except TemplateDoesNotExist:
        response = None
        raise Http404
    return response

def google_site_verification(request, code):
    template_name = 'site_verification/google%s.html' % code
    response = generic_template_view(request, template_name)
    return response

def html_site_verification(request, code):
    template_name = 'site_verification/%s--.html' % code
    response = generic_template_view(request, template_name)
    return response

def bing_site_auth(request):
    template_name = 'site_verification/BingSiteAuth.xml'
    response = generic_template_view(request, template_name, mimetype='text/xml')
    return response

def robots(request):
    template_name = 'robots.txt'
    response = generic_template_view(request, template_name, mimetype='text/plain')
    return response

# Django Imports
from django.http import HttpResponse
from django.test import RequestFactory
from django.test import SimpleTestCase
from django.test import override_settings

# HTK Imports
from htk.middleware import RobotsTagHeaderMiddleware
from htk.view_helpers import add_noindex_page_meta
from htk.view_helpers import set_meta_robots


class RobotsTagHeaderMiddlewareTest(SimpleTestCase):
    @override_settings(ENV_PROD=False)
    def test_non_production_responses_get_noindex_header(self):
        middleware = RobotsTagHeaderMiddleware(lambda request: HttpResponse('ok'))
        request = RequestFactory(HTTP_HOST='demo.example.com').get('/demo')

        response = middleware(request)

        self.assertEqual(
            'noindex, nofollow, noarchive', response['X-Robots-Tag']
        )

    @override_settings(ENV_PROD=True)
    def test_production_success_responses_do_not_get_header(self):
        middleware = RobotsTagHeaderMiddleware(lambda request: HttpResponse('ok'))
        request = RequestFactory(HTTP_HOST='example.com').get('/')

        response = middleware(request)

        self.assertNotIn('X-Robots-Tag', response)

    @override_settings(ENV_PROD=True)
    def test_production_not_found_responses_get_noindex_header(self):
        middleware = RobotsTagHeaderMiddleware(
            lambda request: HttpResponse('not found', status=404)
        )
        request = RequestFactory(HTTP_HOST='example.com').get('/missing')

        response = middleware(request)

        self.assertEqual('noindex, nofollow', response['X-Robots-Tag'])

    @override_settings(
        ENV_PROD=False,
        HTK_NON_PRODUCTION_X_ROBOTS_TAG='noindex, noarchive',
    )
    def test_non_production_header_can_be_customized(self):
        middleware = RobotsTagHeaderMiddleware(lambda request: HttpResponse('ok'))
        request = RequestFactory(HTTP_HOST='demo.example.com').get('/demo')

        response = middleware(request)

        self.assertEqual('noindex, noarchive', response['X-Robots-Tag'])


class RobotsMetaHelpersTest(SimpleTestCase):
    def test_set_meta_robots(self):
        data = {}

        set_meta_robots('noindex,nofollow', data=data)

        self.assertEqual('noindex,nofollow', data['meta']['robots'])

    def test_add_noindex_page_meta_defaults_to_follow(self):
        data = {}

        add_noindex_page_meta(data=data)

        self.assertEqual('noindex,follow', data['meta']['robots'])

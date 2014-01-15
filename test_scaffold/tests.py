import re

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils import unittest

from htk.test_scaffold.helpers import create_test_password
from htk.test_scaffold.helpers import create_test_user
from htk.test_scaffold.models import TestScaffold

class BaseTestCase(unittest.TestCase):
    """Base class for all test cases
    """
    def setUp(self):
        self.assigned_users = 0
        self.users = []
        self._create_batch_test_users()

    def _create_batch_test_users(self):
        for x in xrange(5):
            self.users.append(create_test_user())

    def _assign_test_user(self):
        """Returns:
        a user previously not returned
        """
        if self.assigned_users >= len(self.users):
            self._create_batch_test_users()
        user = self.users[self.assigned_users-1]
        self.assigned_users += 1
        return user

class BaseWebTestCase(BaseTestCase):
    """Base class for other Web test cases
    Sets up some commonly-used parameters
    """
    def setUp(self):
        super(BaseWebTestCase, self).setUp()
        # disable prelaunch mode for unit tests
        scaffold = TestScaffold()
        scaffold.set_fake_prelaunch(prelaunch_mode=False, prelaunch_host=False)

    def _get_user_session(self):
        user = self._assign_test_user()
        password = create_test_password()
        user.set_password(password)
        user.save()
        client = Client()
        success = client.login(username=user.username, password=password)
        self.assertTrue(success)
        return (user, client,)

    def _get(self, view_name, client=None, params=None, follow=False, view_args=None, view_kwargs=None, **extra):
        params = {} if params is None else params
        view_args = [] if view_args is None else view_args
        view_kwargs = {} if view_kwargs is None else view_kwargs
        path = reverse(view_name, args=view_args, kwargs=view_kwargs)
        if type(client) != Client:
            client = Client()
        response = client.get(path, data=params, follow=follow, **extra)
        return response

    def _post(self, view_name, client=None, params=None, follow=False, view_args=None, view_kwargs=None, **extra):
        params = {} if params is None else params
        view_args = [] if view_args is None else view_args
        view_kwargs = {} if view_kwargs is None else view_kwargs
        path = reverse(view_name, args=view_args, kwargs=view_kwargs)
        if type(client) != Client:
            client = Client()
        response = client.post(path, data=params, follow=follow, **extra)
        return response

    def _check_view_is_okay(self, view_name, client=None, params=None, follow=False):
        response = self._get(view_name, client=client, params=params, follow=follow)
        self.assertEqual(200,
                         response.status_code,
                         '[%s] got unexpected response code %d' %
                         (view_name,
                          response.status_code))

    def _check_view_redirects_to_another(self, view_name, another, client=None, params=None, view_args=None, view_kwargs=None, method='get'):
        if method == 'get':
            response = self._get(view_name, client=client, params=params, view_args=view_args, view_kwargs=view_kwargs, follow=True)
        elif method == 'post':
            response = self._post(view_name, client=client, params=params, view_args=view_args, view_kwargs=view_kwargs, follow=True)
        else:
            raise Exception('Unknown HTTP method: %s' % method)
        redirect_chain = response.redirect_chain
        self.assertTrue(len(redirect_chain) > 0,
                        '[%s] did not redirect' % view_name)
        self.assertEqual(302, redirect_chain[0][1])
        if re.match(r'^http://', another):
            # `another` is a full uri
            pattern = another
        else:
            # `another` is a view name
            pattern = r'http://testserver%s' % reverse(another)
        actual = redirect_chain[0][0]
        match = re.match(pattern, actual)
        self.assertIsNotNone(match,
                             '[%s] redirected to [%s] instead of [%s]' %
                             (view_name,
                              actual,
                              another,))

    def _check_view_redirects_to_login(self, view_name, client=None):
        self._check_view_redirects_to_another(view_name, 'account_login', client=client)

    def _check_prelaunch_mode(self, view_name):
        from htk.apps.prelaunch.utils import get_prelaunch_url_name
        prelaunch_url_name = get_prelaunch_url_name()
        self._check_view_redirects_to_another(view_name, get_prelaunch_url_name())

    def test_basic(self):
        self.assertTrue(True)


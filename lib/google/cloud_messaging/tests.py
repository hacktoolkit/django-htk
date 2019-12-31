from django.utils import unittest

from htk.lib.google.cloud_messaging.utils import get_gcm_client
from htk.utils import htk_setting

class GoogleCloudMessagingLibraryTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_gcm_client(self):
        gcm = get_gcm_client()
        if htk_setting('HTK_GCM_API_KEY', None):
            self.assertIsNotNone(gcm)
        else:
            print('No HTK_GCM_API_KEY defined')

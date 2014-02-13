from django.utils import unittest

#import htk.scripts
from htk.scripts import update_static_asset_version

class ScriptsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_update_static_version(self):
        """Test that it runs
        """
        update_static_asset_version.main()

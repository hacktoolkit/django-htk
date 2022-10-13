# HTK Imports
from htk.constants import *
from htk.lib.tests import *
from htk.scripts.tests import *
from htk.test_scaffold.models import TestScaffold
from htk.test_scaffold.tests import (
    BaseTestCase,
    BaseWebTestCase,
)
from htk.utils.tests import *


class HtkWebViewsTestCase(BaseWebTestCase):
    def test_error_pages(self):
        view_names = (
            'error_403',
            'error_404',
            'error_500',
        )
        for view_name in view_names:
            self._check_view_is_okay(view_name)

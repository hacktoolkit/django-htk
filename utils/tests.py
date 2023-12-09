# Python Standard Library Imports
import unittest

# HTK Imports
from htk.compat import has_min_python_version
from htk.utils.text.tests import *  # noqa: F401, F403


if has_min_python_version(3, 6):
    from htk.utils.enums import HtkIntFlag

    class TestHtkIntFlag(unittest.TestCase):
        def test_list_flags(self):
            class TestIntFlag(HtkIntFlag):
                A = 1
                B = 2
                C = 4

            # To combine flags bitwise or is needed
            combined = TestIntFlag.A | TestIntFlag.C

            # 1 | 4 = 5
            self.assertEqual(combined, 5)

            self.assertEqual(combined & TestIntFlag.A, TestIntFlag.A)
            self.assertEqual(combined & TestIntFlag.C, TestIntFlag.C)
            self.assertEqual(combined & TestIntFlag.B, 0)

            self.assertListEqual(
                TestIntFlag.list_flags(combined),
                [TestIntFlag.A, TestIntFlag.C]
            )


if __name__ == '__main__':
    unittest.main()

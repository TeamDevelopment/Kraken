
import unittest

from kraken.core.objects.component_group import ComponentGroup


class TestComponentGroup(unittest.TestCase):

    def testGetName(self):
        pass


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestComponentGroup)


if __name__ == '__main__':
    unittest.main(verbosity=2)

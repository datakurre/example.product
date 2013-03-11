from  example.product.testing import EXAMPLE_PRODUCT_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_test.txt"),
                layer=EXAMPLE_PRODUCT_FUNCTIONAL_TESTING)
    ])
    return suite
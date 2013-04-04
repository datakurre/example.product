from example.product.testing import EXAMPLE_PRODUCT_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_product.robot"),
                layer=EXAMPLE_PRODUCT_FUNCTIONAL_TESTING),
        layered(robotsuite.RobotTestSuite("test_hello.robot"),
                layer=EXAMPLE_PRODUCT_FUNCTIONAL_TESTING)
    ])
    return suite

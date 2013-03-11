from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class ExampleproductLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import example.product
        xmlconfig.file(
            'configure.zcml',
            example.product,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'example.product:default')

EXAMPLE_PRODUCT_FIXTURE = ExampleproductLayer()
EXAMPLE_PRODUCT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXAMPLE_PRODUCT_FIXTURE,),
    name="ExampleproductLayer:Integration"
)
EXAMPLE_PRODUCT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EXAMPLE_PRODUCT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ExampleproductLayer:Functional"
)

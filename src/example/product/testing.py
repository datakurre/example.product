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


try:
    # Inject keyword for getting the selenium session id
    import Selenium2Library
    Selenium2Library.keywords._browsermanagement.\
        _BrowserManagementKeywords.get_session_id = lambda self:\
        self._cache.current.session_id
except ImportError:
    pass


class Keywords(object):

    def report_sauce_status(self, job_id, test_status, test_tags=[]):
        import base64
        import httplib
        import os

        try:
            import json
            json  # pyflakes
        except ImportError:
            import simplejson as json

        username = os.environ.get('SAUCE_USERNAME')
        access_key = os.environ.get('SAUCE_ACCESS_KEY')

        if not job_id:
            return u"No Sauce job id found. Skipping..."
        elif not username or not access_key:
            return u"No Sauce environment variables found. Skipping..."

        token = base64.encodestring('%s:%s' % (username, access_key))[:-1]
        body = json.dumps({'passed': test_status == 'PASS',
                           'tags': test_tags})

        connection = httplib.HTTPConnection('saucelabs.com')
        connection.request('PUT', '/rest/v1/%s/jobs/%s' % (
            username, job_id), body,
            headers={'Authorization': 'Basic %s' % token}
        )

        return connection.getresponse().status

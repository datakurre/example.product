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


import re
import os
import httplib
import base64
try:
    import json
    assert json  # pyflakes
except ImportError:
    import simplejson as json

from robot.libraries.BuiltIn import BuiltIn

USERNAME_ACCESS_KEY = re.compile('^(http|https):\/\/([^:]+):([^@]+)@')


class Keywords:

    def report_sauce_status(self, status, tags=[], remote_url=''):
        """Report test status and tags to SauceLabs
        """
        job_id = BuiltIn().get_library_instance(
            'Selenium2Library')._current_browser().session_id

        if USERNAME_ACCESS_KEY.match(remote_url):
            username, access_key =\
                USERNAME_ACCESS_KEY.findall(remote_url)[0][1:]
        else:
            username = os.environ.get('SAUCE_USERNAME')
            access_key = os.environ.get('SAUCE_ACCESS_KEY')

        if not job_id:
            return u"No Sauce job id found. Skipping..."
        elif not username or not access_key:
            return u"No Sauce environment variables found. Skipping..."

        token = base64.encodestring('%s:%s' % (username, access_key))[:-1]
        body = json.dumps({'passed': status == 'PASS',
                           'tags': tags})

        connection = httplib.HTTPConnection('saucelabs.com')
        connection.request('PUT', '/rest/v1/%s/jobs/%s' % (
            username, job_id), body,
            headers={'Authorization': 'Basic %s' % token}
        )
        return connection.getresponse().status

*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close All Browsers

*** Test Cases ***

Plone site
    [Tags]  start
    Go to  ${PLONE_URL}
    Page should contain  Plone site

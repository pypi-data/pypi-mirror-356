from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.distribution.testing.layer import PloneDistributionFixture
from plone.testing.zope import WSGI_SERVER_FIXTURE


ANSWERS = {
    "site_id": "plone",
    "title": "Plone Site",
    "description": "A Plone Site with Classic UI",
    "site_logo": "name=teste;data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",  # noQA
    "default_language": "en",
    "portal_timezone": "America/Sao_Paulo",
    "setup_content": True,
}


class BaseFixture(PloneDistributionFixture):
    PACKAGE_NAME = "plone.classicui"
    SITES = (("classic", ANSWERS),)
    _distribution_products = (
        ("plone.app.contenttypes", {"loadZCML": True}),
        ("plone.distribution", {"loadZCML": True}),
    )


BASE_FIXTURE = BaseFixture()


class Layer(PloneSandboxLayer):
    defaultBases = (BASE_FIXTURE,)


FIXTURE = Layer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="DistributionLayer:IntegrationTesting",
)

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, WSGI_SERVER_FIXTURE),
    name="DistributionLayer:FunctionalTesting",
)

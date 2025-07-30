
from pytest import fixture
from pytest import skip
import warnings
from datetime import datetime

from depot.io.memory import MemoryFileStorage
from mock import MagicMock
from pytest import fixture

from kotti2 import testing

# Pytest hooks
def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", help="run slow tests")

def pytest_runtest_setup(item):
    if "slow" in item.keywords and not item.config.getoption("--runslow"):
        skip("need --runslow option to run")

# non-public test fixtures

@fixture
def app(db_session, setup_app):
    from webtest import TestApp
    return TestApp(setup_app)

@fixture
def extra_principals(db_session):
    """ Setup additional users 'bob', 'frank' and groups 'bobsgroup' and
    'franksgroup'.  Return the result of ``get_pricipals()``. """
    from kotti2.security import get_principals
    P = get_principals()
    P["bob"] = dict(name="bob", title="Bob")
    P["frank"] = dict(name="frank", title="Frank")
    P["group:bobsgroup"] = dict(name="group:bobsgroup", title="Bob's Group")
    P["group:franksgroup"] = dict(name="group:franksgroup", title="Frank's Group")
    return P

# ---- All fixtures from former __init__.py ----

@fixture
def image_asset():
    """ Return an image file """
    return testing.asset("sendeschluss.jpg")

@fixture
def image_asset2():
    """ Return another image file """
    return testing.asset("logo.png")

@fixture
def allwarnings(request):
    save_filters = warnings.filters[:]
    warnings.filters[:] = []
    yield
    warnings.filters[:] = save_filters

@fixture(scope="session")
def custom_settings():
    return {}

@fixture(scope="session")
def unresolved_settings(custom_settings):
    from kotti2 import conf_defaults
    from kotti2.testing import testing_db_url
    settings = conf_defaults.copy()
    settings["kotti2.secret"] = "secret"
    settings["kotti2.secret2"] = "secret2"
    settings["kotti2.populators"] = "kotti2.testing._populator"
    settings["sqlalchemy.url"] = testing_db_url()
    settings.update(custom_settings)
    return settings

@fixture(scope="session")
def settings(unresolved_settings):
    from kotti2 import _resolve_dotted
    return _resolve_dotted(unresolved_settings)

@fixture
def config(settings):
    from pyramid import testing
    from kotti2 import security
    config = testing.setUp(settings=settings)
    config.include("pyramid_chameleon")
    config.add_default_renderers()
    yield config
    security.reset()
    testing.tearDown()

@fixture(scope="session")
def connection(custom_settings):
    from sqlalchemy import create_engine
    from kotti2 import DBSession
    from kotti2 import metadata
    from kotti2.resources import _adjust_for_engine
    from kotti2.testing import testing_db_url
    engine = create_engine(testing_db_url())
    _adjust_for_engine(engine)
    connection = engine.connect()
    DBSession.registry.clear()
    DBSession.configure(bind=connection)
    metadata.bind = engine
    return connection

@fixture
def content(connection, settings):
    import transaction
    from kotti2 import DBSession
    from kotti2 import metadata
    from kotti2.resources import get_root
    if connection.in_transaction():
        transaction.abort()
    DBSession().close()
    metadata.drop_all(connection.engine)
    transaction.begin()
    metadata.create_all(connection.engine)
    from zope.configuration import xmlconfig
    import kotti2
    xmlconfig.file("workflow.zcml", kotti2, execute=True)
    for populate in settings["kotti2.populators"]:
        populate()
    get_root().path = "/"
    transaction.commit()

@fixture
def db_session(config, content, connection):
    import transaction
    trans = connection.begin()  # begin a non-orm transaction
    from kotti2 import DBSession
    yield DBSession()
    trans.rollback()
    transaction.abort()

@fixture
def dummy_request(config, request, monkeypatch):
    from kotti2.testing import DummyRequest
    marker = request.node.get_closest_marker("user")
    if marker:
        monkeypatch.setattr(DummyRequest, "authenticated_userid", marker.args[0])
    config.manager.get()["request"] = dummy_request = DummyRequest()
    return dummy_request

@fixture
def dummy_mailer(monkeypatch):
    from pyramid_mailer.mailer import DummyMailer
    mailer = DummyMailer()
    monkeypatch.setattr("kotti2.message.get_mailer", lambda: mailer)
    return mailer

@fixture
def events(config):
    from kotti2.events import clear
    config.include("kotti2.events")
    yield config
    clear()

@fixture
def setup_app(unresolved_settings, filedepot):
    from kotti2 import base_configure
    config = base_configure({}, **unresolved_settings)
    return config.make_wsgi_app()

@fixture
def app(workflow, db_session, dummy_mailer, events, setup_app):
    from webtest import TestApp
    return TestApp(setup_app)

@fixture
def browser(db_session, request, setup_app):
    from zope.testbrowser.wsgi import Browser
    from kotti2.testing import BASE_URL
    host, port = BASE_URL.split(":")[-2:]
    browser = Browser("http://{}:{}/".format(host[2:], int(port)), wsgi_app=setup_app)
    marker = request.node.get_closest_marker("user")
    if marker:
        from pyramid.security import remember
        from pyramid.testing import DummyRequest
        login = marker.args[0]
        environ = dict(HTTP_HOST=host[2:])
        for _, value in remember(DummyRequest(environ=environ), login):
            cookie, _ = value.split(";", 1)
            name, value = cookie.split("=")
            if name in browser.cookies:
                del browser.cookies[name]
            browser.cookies.create(name, value.strip('"'), path="/")
    return browser

@fixture
def root(db_session):
    from kotti2.resources import get_root
    return get_root()

@fixture
def webtest(app, monkeypatch, request, filedepot, dummy_mailer):
    from webtest import TestApp
    marker = request.node.get_closest_marker("user")
    if marker:
        login = marker.args[0]
        monkeypatch.setattr(
            "pyramid.authentication."
            "AuthTktAuthenticationPolicy.unauthenticated_userid",
            lambda self, req: login,
        )
    return TestApp(app)

@fixture
def workflow(config):
    from zope.configuration import xmlconfig
    import kotti2
    xmlconfig.file("workflow.zcml", kotti2, execute=True)

class TestStorage(MemoryFileStorage):
    def __bool__(self):
        return True
    def get(self, file_or_id):
        f = super().get(file_or_id)
        f.last_modified = datetime(2012, 12, 30)
        return f

@fixture
def depot_tween(config, dummy_request):
    from depot.manager import DepotManager
    from kotti2.filedepot import TweenFactory
    from kotti2.filedepot import uploaded_file_response
    from kotti2.filedepot import uploaded_file_url
    dummy_request.__class__.uploaded_file_response = uploaded_file_response
    dummy_request.__class__.uploaded_file_url = uploaded_file_url
    _set_middleware = DepotManager.set_middleware
    TweenFactory(None, config.registry)
    @classmethod
    def set_middleware_patched(cls, mw):
        pass
    DepotManager.set_middleware = set_middleware_patched
    yield DepotManager
    DepotManager.set_middleware = _set_middleware

@fixture
def mock_filedepot(depot_tween):
    from depot.manager import DepotManager
    DepotManager._depots = {"mockdepot": MagicMock(wraps=TestStorage())}
    DepotManager._default_depot = "mockdepot"
    yield DepotManager
    DepotManager._clear()

@fixture
def filedepot(db_session, depot_tween):
    from depot.manager import DepotManager
    DepotManager._depots = {"filedepot": MagicMock(wraps=TestStorage())}
    DepotManager._default_depot = "filedepot"
    yield DepotManager
    db_session.rollback()
    DepotManager._clear()

@fixture
def no_filedepots(db_session, depot_tween):
    from depot.manager import DepotManager
    DepotManager._depots = {}
    DepotManager._default_depot = None
    yield DepotManager
    db_session.rollback()
    DepotManager._clear()

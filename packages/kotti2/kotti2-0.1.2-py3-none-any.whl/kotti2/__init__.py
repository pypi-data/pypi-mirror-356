import os.path

import pkg_resources
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import BeforeRender
from pyramid.util import DottedNameResolver
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import MetaData
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register

try:
    from pyramid.threadlocal import get_current_registry
except ImportError:
    from pyramid.registry import global_registry as get_current_registry

from kotti2.sqla import Base as KottiBase

metadata = MetaData()
DBSession = scoped_session(sessionmaker(autoflush=True))
register(DBSession)
Base = declarative_base(cls=KottiBase)
Base.metadata = metadata
Base.query = DBSession.query_property()
TRUE_VALUES = ("1", "y", "yes", "t", "true")
FALSE_VALUES = ("0", "n", "no", "f", "false", "none")


def authtkt_factory(**settings):
    from kotti2.security import list_groups_callback

    kwargs = dict(
        secret=settings["kotti2.secret2"],
        hashalg="sha512",
        callback=list_groups_callback,
    )
    try:
        return AuthTktAuthenticationPolicy(**kwargs)
    except TypeError:
        # BBB with Pyramid < 1.4
        kwargs.pop("hashalg")
        return AuthTktAuthenticationPolicy(**kwargs)


def acl_factory(**settings):
    return ACLAuthorizationPolicy()


def beaker_session_factory(**settings):
    return session_factory_from_settings(settings)


def none_factory(**kwargs):  # pragma: no cover
    return None


# All of these can be set by passing them in the Paste Deploy settings:
conf_defaults = {
    "kotti2.alembic_dirs": "kotti2:alembic",
    "kotti2.asset_overrides": "",
    "kotti2.authn_policy_factory": "kotti2.authtkt_factory",
    "kotti2.authz_policy_factory": "kotti2.acl_factory",
    "kotti2.available_types": " ".join(
        ["kotti2.resources.Document", "kotti2.resources.File"]
    ),
    "kotti2.base_includes": " ".join(
        [
            "kotti2",
            "kotti2.traversal",
            "kotti2.filedepot",
            "kotti2.events",
            "kotti2.sanitizers",
            "kotti2.views",
            "kotti2.views.cache",
            "kotti2.views.view",
            "kotti2.views.edit",
            "kotti2.views.edit.actions",
            "kotti2.views.edit.content",
            "kotti2.views.edit.default_views",
            "kotti2.views.edit.upload",
            "kotti2.views.file",
            "kotti2.views.login",
            "kotti2.views.navigation",
            "kotti2.views.users",
        ]
    ),
    "kotti2.caching_policy_chooser": (
        "kotti2.views.cache.default_caching_policy_chooser"
    ),
    "kotti2.configurators": "",
    "kotti2.date_format": "medium",
    "kotti2.datetime_format": "medium",
    "kotti2.depot_mountpoint": "/depot",
    "kotti2.depot_replace_wsgi_file_wrapper": False,
    "kotti2.depot.0.backend": "kotti2.filedepot.DBFileStorage",
    "kotti2.depot.0.name": "dbfiles",
    "kotti2.fanstatic.edit_needed": "kotti2.fanstatic.edit_needed",
    "kotti2.fanstatic.view_needed": "kotti2.fanstatic.view_needed",
    "kotti2.login_success_callback": "kotti2.views.login.login_success_callback",
    "kotti2.max_file_size": "10",
    "kotti2.modification_date_excludes": " ".join(["kotti2.resources.Node.position"]),
    "kotti2.populators": "kotti2.populate.populate",
    "kotti2.principals_factory": "kotti2.security.principals_factory",
    "kotti2.register": "False",
    "kotti2.register.group": "",
    "kotti2.register.role": "",
    "kotti2.request_factory": "kotti2.request.Request",
    "kotti2.reset_password_callback": "kotti2.views.login.reset_password_callback",  # noqa
    "kotti2.root_factory": "kotti2.resources.default_get_root",
    "kotti2.sanitizers": " ".join(
        [
            "xss_protection:kotti2.sanitizers.xss_protection",
            "minimal_html:kotti2.sanitizers.minimal_html",
            "no_html:kotti2.sanitizers.no_html",
        ]
    ),
    "kotti2.sanitize_on_write": " ".join(
        [
            "kotti2.resources.Document.body:xss_protection",
            "kotti2.resources.Content.title:no_html",
            "kotti2.resources.Content.description:no_html",
        ]
    ),
    "kotti2.search_content": "kotti2.views.util.default_search_content",
    "kotti2.session_factory": "kotti2.beaker_session_factory",
    "kotti2.static.edit_needed": "",  # BBB
    "kotti2.static.view_needed": "",  # BBB
    "kotti2.templates.api": "kotti2.views.util.TemplateAPI",
    "kotti2.time_format": "medium",
    "kotti2.url_normalizer": "kotti2.url_normalizer.url_normalizer",
    "kotti2.url_normalizer.map_non_ascii_characters": True,
    "kotti2.use_tables": "",
    "kotti2.use_workflow": "kotti2:workflow.zcml",
    "kotti2.zcml_includes": " ".join([]),
    "pyramid.includes": "",
    "pyramid_deform.template_search_path": "kotti2:templates/deform",
}

conf_dotted = {
    "kotti2.authn_policy_factory",
    "kotti2.authz_policy_factory",
    "kotti2.available_types",
    "kotti2.base_includes",
    "kotti2.caching_policy_chooser",
    "kotti2.configurators",
    "kotti2.fanstatic.edit_needed",
    "kotti2.fanstatic.view_needed",
    "kotti2.login_success_callback",
    "kotti2.modification_date_excludes",
    "kotti2.populators",
    "kotti2.principals_factory",
    "kotti2.request_factory",
    "kotti2.reset_password_callback",
    "kotti2.root_factory",
    "kotti2.search_content",
    "kotti2.session_factory",
    "kotti2.templates.api",
    "kotti2.url_normalizer",
}


def get_version():
    return pkg_resources.require("Kotti2")[0].version


def get_settings():
    return get_current_registry().settings


def _resolve_dotted(d, keys=conf_dotted):
    resolved = d.copy()

    for key in keys:
        value = resolved[key]
        if not isinstance(value, str):
            continue
        new_value = []
        for dottedname in value.split():
            new_value.append(DottedNameResolver().resolve(dottedname))
        resolved[key] = new_value

    return resolved


def main(global_config, **settings):
    # This function is a 'paste.app_factory' and returns a WSGI
    # application.

    from kotti2.resources import initialize_sql

    config = base_configure(global_config, **settings)
    engine = engine_from_config(config.registry.settings)
    initialize_sql(engine)
    return config.make_wsgi_app()


def base_configure(global_config, **settings):
    # Resolve dotted names in settings, include plug-ins and create a
    # Configurator.

    from kotti2.resources import get_root

    for key, value in conf_defaults.items():
        settings.setdefault(key, value)

    for key, value in settings.items():
        if key.startswith("kotti2") and isinstance(value, bytes):
            settings[key] = value.decode("utf8")

    # Allow extending packages to change 'settings' w/ Python:
    k = "kotti2.configurators"
    for func in _resolve_dotted(settings, keys=(k,))[k]:
        func(settings)

    settings = _resolve_dotted(settings)
    secret1 = settings["kotti2.secret"]
    settings.setdefault("kotti2.secret2", secret1)

    # We'll process ``pyramid_includes`` later by hand, to allow
    # overrides of configuration from ``kotti2.base_includes``:
    pyramid_includes = settings.pop("pyramid.includes", "")

    config = Configurator(
        request_factory=settings["kotti2.request_factory"][0], settings=settings
    )
    config.begin()

    config.hook_zca()
    config.include("pyramid_zcml")

    # Chameleon bindings were removed from Pyramid core since pyramid>=1.5a2
    config.include("pyramid_chameleon")

    config.registry.settings["pyramid.includes"] = pyramid_includes

    # Include modules listed in 'kotti2.base_includes':
    for module in settings["kotti2.base_includes"]:
        config.include(module)
    config.commit()

    # Modules in 'pyramid.includes' and 'kotti2.zcml_includes' may
    # override 'kotti2.base_includes':
    if pyramid_includes:
        for module in pyramid_includes.split():
            config.include(module)

    for name in settings["kotti2.zcml_includes"].strip().split():
        config.load_zcml(name)

    config.commit()

    config._set_root_factory(get_root)

    return config


def includeme(config):
    """ Pyramid includeme hook.

    :param config: app config
    :type config: :class:`pyramid.config.Configurator`
    """

    import kotti2.views.util

    settings = config.get_settings()

    authentication_policy = settings["kotti2.authn_policy_factory"][0](**settings)
    authorization_policy = settings["kotti2.authz_policy_factory"][0](**settings)
    session_factory = settings["kotti2.session_factory"][0](**settings)
    if authentication_policy:
        config.set_authentication_policy(authentication_policy)
    if authorization_policy:
        config.set_authorization_policy(authorization_policy)
    config.set_session_factory(session_factory)

    config.add_subscriber(kotti2.views.util.add_renderer_globals, BeforeRender)

    for override in [
        a.strip() for a in settings["kotti2.asset_overrides"].split() if a.strip()
    ]:
        config.override_asset(to_override="kotti2", override_with=override)

    config.add_translation_dirs(f"{os.path.dirname(__file__)}/locale")
    # used to be
    # config.add_translation_dirs("kotti2:locale")
    # which fails with recent pytest (works in non testing though)

    workflow = settings["kotti2.use_workflow"]
    if workflow.lower() not in FALSE_VALUES:
        config.load_zcml(workflow)

    return config

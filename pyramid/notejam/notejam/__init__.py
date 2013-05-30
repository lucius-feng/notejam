from pyramid.config import Configurator
from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    RootFactory
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    session_factory = UnencryptedCookieSessionFactoryConfig(
        settings['session.secret']
    )

    authn_policy = SessionAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()

    Base.metadata.bind = engine
    config = Configurator(
        settings=settings,
        root_factory=RootFactory,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory
    )
    config.add_static_view('static', 'static', cache_max_age=3600)
    # routes
    config.add_route('home', '/')
    config.add_route('notes', '/notes/')
    config.add_route('signin', '/signin/')
    config.add_route('signout', '/signout/')
    config.add_route('signup', '/signup/')
    config.scan()
    return config.make_wsgi_app()
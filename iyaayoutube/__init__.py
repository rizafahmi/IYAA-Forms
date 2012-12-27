from pyramid.config import Configurator
from pyramid.mako_templating import renderer_factory as mako_factory
from pyramid.events import NewRequest


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_renderer('.html', mako_factory)

    config.add_route('home', '/')
    config.add_route('home2', '/phase2')
    config.add_route('home1', '/phase1')
    config.add_route('form', '/form')
    config.add_route('countdown', '/countdown')
    config.add_route('save', '/save')
    config.add_route('list', '/list')
    config.add_route('list2', '/list2')
    config.add_route('cleanlist2', '/cleanlist2')
    config.add_route('list_null', '/list_null')
    config.add_route('noaccess', '/noaccess')
    config.add_route('pilih', '/pilih')
    config.add_route('result', '/result')
    config.add_route('email_list', '/email_list')
    config.add_route('duplicate_list', '/duplicate_list')
    config.add_route('duplicate_list2', '/duplicate_list2')
    config.add_route('search', '/search')
    # Admin List

    # MongoDB Setting
    import pymongo
    from urlparse import urlparse

    db_url = urlparse(settings['mongo_uri'])
    conn = pymongo.Connection(host=db_url.hostname, port=db_url.port)
    config.registry.settings['db_conn'] = conn

    def add_mongo_db(event):
        settings = event.request.registry.settings
        db = settings['db_conn'][db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)

        event.request.db = db

    config.add_subscriber(add_mongo_db, NewRequest)

    config.scan()
    return config.make_wsgi_app()

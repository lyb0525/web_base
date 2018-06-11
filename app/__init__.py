# coding=utf-8

import time

from flask import Flask, g

from app.foundation import db

from app import apis

DEFAULT_APP_NAME = 'app'


def create_app():
    app = Flask(DEFAULT_APP_NAME)
    app.debug = True
    app.config.from_object('config')
    configure_foundations(app)
    configure_blueprint(app, apis.MODULES)
    return app


def configure_foundations(app):

    db.app = app
    db.init_app(app)

    @app.before_request
    def before_request():
        now = int(time.time())
        g.TIMESTAMP = now

    @app.teardown_appcontext
    def release_sessions(*args, **kwargs):
        db.session.close()


def configure_handlers(app):

    @app.errorhandler(403)
    def abandon(e):
        return {'err_msg': str(e)}, 403


def configure_blueprint(app, modules):
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


app = create_app()

# if not app.debug:
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     stream_handler = logging.StreamHandler()
#     app.logger.addHandler(stream_handler)
#

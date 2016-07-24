# coding=utf-8
import json
from datetime import date
import time

from flask import Flask, g, render_template
from app import views

DEFAULT_APP_NAME = 'app'
def create_app():
    app = Flask(DEFAULT_APP_NAME)
    app.debug = True
    app.config.from_object('config')
    configure_foundations(app)
    configure_blueprint(app, views.MODULES)
    return app

def configure_foundations(app):
    # celery.init_app(app)

    @app.before_request
    def before_request():
        now = int(time.time())
        g.TIMESTAMP = now

def configure_handlers(app):
    @app.errorhandler(403)
    def abandon(e):
        return render_template('page/error/403.html', username=g.user.username if
        g.user.is_authenticated() else ''), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('page/error/404.html', username=g.user.username if
        g.user.is_authenticated() else ''), 404

    @app.errorhandler(500)
    def error(e):
        return render_template('page/error/500.html', username=g.user.username if
        g.user.is_authenticated() else '', ), 500

    @app.errorhandler(400)
    def bad_request(e):
        return render_template('page/error/400.html', username=g.user.username if
        g.user.is_authenticated() else ''), 400


def configure_blueprint(app, modules):
    for module in modules:
        app.register_blueprint(module)


def configure_template_filter(app):
    import math

    @app.template_filter('dateint')
    def _jinja2_filter_dateint(dateint):
        return date.fromordinal(dateint).strftime('%Y-%m-%d')

    @app.template_filter('timestamp')
    def _jinja2_filter_timestamp(timestamp):
        import time

        timetuple = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timetuple)

    @app.template_filter('date')
    def _jinja2_filter_date(timestamp):
        import time

        timetuple = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d', timetuple)

    @app.template_filter('percent')
    def _jinja2_filter_percent(f, digits=0):
        tmp = f * (10 ** (2 + digits))
        tmp = math.floor(tmp)
        if digits > 0:
            return "%s%%" % (tmp / (10 ** digits))
        else:
            return "%d%%" % tmp

    @app.template_filter('json')
    def _jinja2_json(obj):
        return json.dumps(obj)

    @app.template_filter('currency')
    def _jinja2_currency(n):
        return str(n) + u'元'


app = create_app()

# if not app.debug:
#     import logging
#     logging.basicConfig(level=logging.INFO)
#     stream_handler = logging.StreamHandler()
#     app.logger.addHandler(stream_handler)
#

"""editable_flask"""

from flask import request, jsonify
from jinja2.environment import copy_cache
from jinja2 import Environment, BaseLoader
from collections import OrderedDict
import json
import os
from .editable import EditableExtension
from .views import edits

class Edits(object):
    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Register the Jinja extension, load edits from app.config['EDITS_PATH'],
        and register blueprints.

        :param app:
            Flask application instance
        """
        @app.template_filter('appconfig')
        def appconfig(value):
            required_config = app.config.get(value)
            return required_config
        
        app.config.setdefault('APP_NAME', 'EditableFlask')
        app.config.setdefault('APP_STATIC_FOLDER', os.path.basename(app.static_folder))
        app.config.setdefault('APP_NAME_HTML', 'EditableFlask')
        app.config.setdefault('EDITS_URL', '/edits')
        app.config.setdefault('EDITS_PREVIEW', False)
        app.config.setdefault('EDITS_SUMMERNOTE', False)
        app.config.setdefault('LOGIN_ROUTE', '/login')
        app.config.setdefault('LOGIN_FOOTER', 'Powered by EditableFlask created with ❤️‍🔥 by <a href="https://github.com/MahirShah07">Mahir Shah</a>')

        if 'FILE_PATH' not in app.config:
            raise Exception('FILE_PATH not set in app configuration.')
        EDITS_PATH = app.config['FILE_PATH']+'/edits.json'
        if not os.path.isfile(EDITS_PATH):
            with open(EDITS_PATH, 'w') as f:
                json.dump({}, f)
        if os.path.isfile(EDITS_PATH):
            with open(EDITS_PATH) as f:
                _db = json.loads(f.read(), object_pairs_hook=OrderedDict)
        else:
            _db = OrderedDict()
        
        from .conditions import CONDITIONS 
        CONDITIONS(app, edits)

        env = Environment(loader=BaseLoader())
        app.jinja_env.add_extension(EditableExtension)
        app.jinja_env.edits = _db
        app.jinja_env.edits_preview = app.config['EDITS_PREVIEW']
        app.jinja_env.edits_cache = copy_cache(app.jinja_env.cache)
        if app.config['EDITS_PREVIEW']:
            app.jinja_env.cache = None

        app.register_blueprint(edits, url_prefix=app.config['EDITS_URL'])

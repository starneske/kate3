# pylint: skip-file
"""
Add docstring here
"""
import json
import os

from flask import Blueprint, render_template, send_from_directory
from pkg_resources import resource_filename


def get_swaggerui_blueprint(base_url, api_url, config=None):
    """
    Add docstring here
    """

    swagger_ui = Blueprint('swagger_ui',
                           __name__,
                           static_folder=resource_filename(
                               'qube.src.resources', 'assets'),
                           template_folder=resource_filename(
                               'qube.src.resources', 'templates'))

    default_config = {
        'client_realm': 'null',
        'client_id': 'null',
        'client_secret': 'null',
        'app_name': 'null',
        'docExpansion': "none",
        'jsonEditor': False,
        'defaultModelRendering': 'schema',
        'showRequestHeaders': False,
        'supportedSubmitMethods': ['get', 'post', 'put', 'delete', 'patch']
    }

    if config:
        default_config.update(config)

    fields = {
        # Some fields are used in functions etc, so we treat them special
        'base_url': base_url,
        'api_url': api_url,
        'app_name': default_config.pop('app_name'),
        'client_realm': default_config.pop('client_realm'),
        'client_id': default_config.pop('client_id'),
        'client_secret': default_config.pop('client_secret'),

        # Rest are just serialized into json string for inclusion in .js file
        'config_json': json.dumps(default_config)
    }

    @swagger_ui.route('/')
    @swagger_ui.route('/<path:path>')
    def show(path=None):
        if not path or path == 'index.html':
            return render_template('index.template.html', **fields)
        else:
            return send_from_directory(
                # A bit of a hack to not pollute the default
                # /static path with our files.
                os.path.join(
                    swagger_ui.root_path,
                    swagger_ui._static_folder
                ),
                path
            )

    return swagger_ui

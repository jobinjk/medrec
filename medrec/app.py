from flask import Flask, render_template

from medrec import auth, api
from medrec.extensions import db, jwt  # , conf_celery
from medrec.config import conf
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import os


def create_app(config=None, testing=False, cli=False):
    '''Application factory, used to create application
    '''
    app = Flask('medrec')

    configure_app(app, testing)
    configure_extensions(app, cli)
    register_blueprints(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


def configure_app(app, testing=False):
    '''set configuration for application
    '''
    # default configuration
    app.config.from_object(conf[os.getenv('MEDREC_CONFIG', 'default')])

    if testing is True:
        # override with testing config
        app.config.from_object('medrec.configtest')
    else:
        # override with env variable, fail silently if not set
        app.config.from_envvar(
            'MEDREC_CONFIG', silent=True)


def configure_extensions(app, cli):
    '''configure flask extensions
    '''
    db.init_app(app)
    jwt.init_app(app)
    # celery = conf_celery(app)

    # Configue cors for localhost
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin',
                             'http://0.0.0.0:8080/')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,OPTIONS,DELETE,PATCH,POST,DELETE')
        print(response)
        return response

    # if app.config['ENABLE_SHARDING']:

    #     # Enable sharding
    #     client = MongoClient(app.config['HOST'])
    #     try:
    #         client.admin.command('enableSharding', app.config['DB'])
    #     except OperationFailure:
    #         pass

    #     try:
    #         client.admin.command(
    #             'shardCollection', 'MEDREC.report_data', key={'_id': 1})
    #         client.admin.command(
    #             'shardCollection', 'MEDREC.reports', key={'_id': 1})
    #     except OperationFailure:
    #         pass


def register_blueprints(app):
    '''register all blueprints for application
    '''
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)

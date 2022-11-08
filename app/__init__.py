import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_babelex import Babel
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config import get_config_obj, SYS_NAME, ROOT_URL

logger = logging.getLogger()
db = SQLAlchemy()
migrate = Migrate(render_as_batch=True)  # to solve alter-issue of sqlite
bootstrap = Bootstrap()
babel = Babel()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name=None):
    if config_name is None:
        import os
        config_name = os.getenv("FLASK_ENV", 'default')
    config_obj = get_config_obj(config_name)

    app = Flask(__name__)

    app.config.from_object(config_obj)
    logger.info(f'loading config of {config_name}, db type is: {config_obj.get_database_type()}')
    config_obj.init_app(app)

    db.init_app(app)
    babel.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    """blueprint registry"""
    logger.info('register blueprints and views')
    from . import views
    views.init_app(app, SYS_NAME)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    logger.info('create_app done!')

    return app

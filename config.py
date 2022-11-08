import logging
import os
from pathlib import Path
from datetime import timedelta
"""
System Configuration
"""

"""
Base directory path of the project.
"""
base_dir = Path.cwd()

"""
System name, showing as brand at the top navbar.
"""
SYS_NAME: str = 'AdminExpress'

"""
When sidebar collapsed, the system name would change to SYS_NAME_SHORT, in order to adapt the width of brand zone.
The length of SYS_NAME_SHORT would be no more than 3 chars for a better view.
You can change to a smaller company logo as well.
"""
SYS_NAME_SHORT: str = 'AE'

"""
ROOT_URL follows the domain, which might be a website.
e.g., when set ROOT_URL='/admin', the full url address would be: http://127.0.0.1/root_url, 
"""
ROOT_URL: str = '/admin'  # 网址根路径名

"""
New registered user account may need to be audited by the administrator.
Set USER_AUDIT_ENABLED to enable/disable the audit process.
"""
USER_AUDIT_ENABLED = True  # 用户注册后是否需审核

"""
set database url string as system environment variable
"""
ENV_DATABASE_URL_KEY = 'AE_DATABASE_URL'

"""
Define prefix of all system-table-names, in order to separate business-tables from system-tables.
"""
default_tab_prefix: str = 'AE_'

"""
sqlite would be used as the default database
"""
default_db_conn = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')

"""
upload_path for saving files uploaded.
"""
upload_path = base_dir.joinpath('uploads')

"""
log_path for system logs
"""
log_path = base_dir.joinpath('logs')

"""
base_config_path for sqls and other configuration-files.
"""
base_config_path = base_dir.joinpath('configs')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'SomeWordsHardToGuess&ChangeMe!!!'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 600
    SQLALCHEMY_DATABASE_URI = None

    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    BOOTSTRAP_SERVE_LOCAL = True

    """
    bootswatch themes, optional at flask_admin/static/bootstrap/../swatch
    """
    FLASK_ADMIN_SWATCH = 'simplex'
    FLASK_ADMIN_FLUID_LAYOUT = True
    BABEL_DEFAULT_LOCALE = 'zh_CN'  # i18n with Flask-BabelEx
    LOG_PATH = log_path
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10
    LOG_LEVEL_DEFAULT = logging.INFO

    @staticmethod
    def init_app(app):
        pass

    def get_database_type(self):
        if self.SQLALCHEMY_DATABASE_URI is not None:
            return self.SQLALCHEMY_DATABASE_URI.split(':')[0].split('+')[0]

        return None


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(ENV_DATABASE_URL_KEY) or default_db_conn


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(ENV_DATABASE_URL_KEY) or default_db_conn
    # SQLALCHEMY_DATABASE_URI = "mysql://..."


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config_obj(config_name=None):
    config_clazz = config.get(config_name)
    if config_clazz is None:
        config_clazz = config.get('default')

    config_obj = config_clazz()
    return config_obj


if __name__ == '__main__':
    dev_config = config['test']()
    print('db-type of test is', dev_config.get_database_type())

    config_object = get_config_obj()
    print(config_object.get_database_type())

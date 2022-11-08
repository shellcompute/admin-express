import yaml
import os
import re
from flask import current_app
from config import base_config_path

"""
根据 sql_id 自动从对应的 sql脚本中加载 sqltext
sql脚本默认位置：configs/[mysql|oracle|postgresql]/sqlscripts.yml
"""


def get_sql_by_id(sql_id):
    sqls = YamlLoader(current_app)
    return sqls.get_sql_text(sql_id)


def get_db_type(app):
    """获取当前数据库类型，如：oracle/mysql/postgresql..."""
    if app.config and app.config.get('SQLALCHEMY_DATABASE_URI'):
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        db_type = re.split('[+:]', db_uri)[0]
    else:
        db_type = 'mysql'

    return db_type.lower()


class YamlLoader:
    """
    yaml file loader
    """
    def __init__(self, app=None, filename=None):
        if app is not None and filename is None:
            file_path = os.path.join(base_config_path, get_db_type(app))
            self.filename = os.path.join(file_path, 'sql_scripts.yml')
        else:
            self.filename = filename

        print('filename:', self.filename)

        with open(self.filename, encoding="utf-8") as f:
            self.config_data = yaml.full_load(f)

    def get_data(self, section, option=None):
        if option is None:
            return self.config_data[section]
        else:
            return self.config_data[section][option]

    def get_sql_text(self, sql_id):
        return self.config_data[sql_id]


if __name__ == '__main__':
    sql_file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                 'configs/mysql/sqlscripts.yml')
    yl = YamlLoader(filename=sql_file_name)
    print(yl.get_sql_text('rpt01'))

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, DateTime, String
# from sqlalchemy.schema import Identity

from app import db
from config import default_tab_prefix

TAB_PREFIX = default_tab_prefix if default_tab_prefix is not None else 'T_'


class BaseModel(db.Model):
    __abstract__ = True
    """
    数据模型基类

    不同数据库，在处理ID自增时有不同做法
    当为sqlite/mysql时：
    id = Column(Integer, primary_key=True, autoincrement=True)
    当为 Oracle 或 MSSQL时：
    id = Column(Integer, Identity(start=1), primary_key=True)
    """
    # id = Column(Integer, Identity(start=1), primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=True, default=datetime.now)
    updated_at = Column(DateTime, nullable=True, default=datetime.now)
    created_by = Column(String(50), nullable=True)
    updated_by = Column(String(50), nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def get_table_name(self):
        return getattr(self, '__tablename__', None)


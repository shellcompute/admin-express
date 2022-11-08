from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql.sqltypes import String, Integer
from app.core.base_model import BaseModel, TAB_PREFIX


class Resource(BaseModel):
    __tablename__ = TAB_PREFIX + 'resource'
    resource_code = Column(String(128), nullable=False)
    resource_name = Column(String(128), nullable=False)
    resource_type = Column(String(12), nullable=False, default='VIEW')
    parent_id = Column(Integer, nullable=True)
    url = Column(String(256), nullable=True)

    def __init__(self, resource_code, resource_name, resource_type=None, parent_id=None, url=None):
        self.resource_code = resource_code
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.parent_id = parent_id
        self.url = url

    def __repr__(self):
        return '<%s %s>' % (self.resource_type, self.resource_name)


class Role(BaseModel):
    __tablename__ = TAB_PREFIX + 'role'
    role_code = Column(String(128), nullable=False)
    role_name = Column(String(128), nullable=False)
    resources = relationship('Resource', secondary=TAB_PREFIX + 'role_resources',
                             backref=backref('Role', lazy='subquery'))

    def __init__(self, role_code, role_name):
        self.role_code = role_code
        self.role_name = role_name

    def __repr__(self):
        return '<Role %s>' % self.role_name


class RoleResources(BaseModel):
    __tablename__ = TAB_PREFIX + 'role_resources'
    role_id = Column(Integer, ForeignKey(TAB_PREFIX + 'role.id'))
    resource_id = Column(Integer, ForeignKey(TAB_PREFIX + 'resource.id'))


class UserRoles(BaseModel):
    __tablename__ = TAB_PREFIX + 'user_roles'
    user_id = Column(Integer, ForeignKey(TAB_PREFIX + 'user.id'))
    role_id = Column(Integer, ForeignKey(TAB_PREFIX + 'role.id'))

from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.sqltypes import String, DateTime
from app.core.base_model import BaseModel, TAB_PREFIX
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager


class User(BaseModel, UserMixin):
    __tablename__ = TAB_PREFIX + 'user'
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False, server_default='')
    activated = Column(String(1), nullable=False, server_default='0')  # 0-否，A-已审核，1-是
    is_locked = Column(String(1), nullable=True)  # 1-已锁定，null或0-未锁定
    lock_time = Column(DateTime, nullable=True)
    realname = Column(String(255))
    email = Column(String(255))
    email_confirm_at = Column(DateTime, nullable=True)
    mobile = Column(String(50))
    mobile_confirm_at = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    pwd_set_time = Column(DateTime, nullable=True)
    roles = relationship('Role', secondary=TAB_PREFIX + 'user_roles', backref=backref('User', lazy='dynamic'))

    def __init__(self, username, password, realname=None, email=None, mobile=None):
        self.username = username
        self.realname = realname
        self.mobile = mobile
        self.email = email
        self.activated = '0'
        self.password_hash = generate_password_hash(password)

    @property  # 设置password为只读
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter  # 设置密码hash
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        # self.pwd_set_time = datetime.now()

    def verify_password(self, password):  # 验证密码hash
        return check_password_hash(self.password_hash, password)

    @login_manager.user_loader  # 是否登录验证
    def load_user(user_id):
        return User.query.filter_by(id=int(user_id)).first()

    def __repr__(self):
        return '[%r]%s' % (self.id, self.username)

    def get_resources(self):
        resources = []
        for role in self.roles:
            for resource in role.resources:
                if resource.resource_type == 'VIEW' and resource.resource_code not in resources:
                    resources.append(resource.resource_code)

        # print(resources)
        return resources


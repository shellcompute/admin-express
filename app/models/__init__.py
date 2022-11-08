from app import db
from .resources import Resource, RoleResources, Role, UserRoles
from .user import User
from .article import Article


def init_admin():
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user is None:
        """auto create admin user account"""
        admin_user = User(username='admin', password='Abcd@1234', realname='Admin', email='', mobile='')
        admin_user.activated = '1'
        db.session.add(admin_user)
        db.session.commit()
    else:
        print('admin account has been created already!')

    admin_role = Role.query.filter_by(role_code='ADMIN').first()
    if admin_role is None:
        """auto create admin role"""
        admin_role = Role(role_code='ADMIN', role_name='系统管理员')
        admin_user.roles = [admin_role]
        db.session.add(admin_role)
        db.session.commit()
    else:
        if admin_user.roles is None or admin_role not in admin_user.roles:
            admin_user.roles = [admin_role]
            # db.session.add(admin_role)
            db.session.commit()

        print('admin role has been created already!')

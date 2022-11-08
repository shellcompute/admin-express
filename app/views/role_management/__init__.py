from flask_admin.menu import MenuCategory
from app.models import *
from app import db
from .role_view import UserView, RoleView, ResourceView


def add_views(sys_admin):
    sys_admin.add_category('用户管理', icon_type='glyph', icon_value='glyphicon-user')
    sys_admin.add_view(ResourceView(Resource, db.session, name="资源管理", category='用户管理', menu_icon_type='glyph',
                                    menu_icon_value='glyphicon-tree-deciduous'))
    sys_admin.add_view(RoleView(Role, db.session, name="角色管理", category='用户管理',menu_icon_type='glyph',
                                menu_icon_value='glyphicon-th'))
    # sys_admin.add_view(RoleResourceView(RoleResources, db.session, name="角色资源管理", category='用户管理'))
    sys_admin.add_view(UserView(User, db.session, name="用户管理", category='用户管理', menu_icon_type='glyph',
                                menu_icon_value='glyphicon-user'))


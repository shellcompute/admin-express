from flask import Blueprint
from flask_admin.menu import MenuLink, MenuCategory, SubMenuCategory

auth = Blueprint('auth', __name__)

from . import views, errors


def add_views(sys_admin):
    sys_admin.add_link(MenuLink(name='修改密码', class_name='dropdown', icon_type='glyph', icon_value='glyphicon-wrench',
                                url='/auth/change_pass'))
    sys_admin.add_link(MenuLink(name='Log Out', icon_type='glyph', icon_value='glyphicon-log-out', url='/auth/logout'))

from flask_admin import Admin
from config import ROOT_URL

all_views = []


def init_app(app, name):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .index import HomeView
    sys_admin = Admin(app, name=name, template_mode='bootstrap3',
                      url=ROOT_URL,
                      index_view=HomeView(url=ROOT_URL))

    from .auth import add_views as au_add_views
    au_add_views(sys_admin)

    """文章管理"""
    from .articles import add_views as article_add_views
    article_add_views(sys_admin)

    """用户管理"""
    from .role_management import add_views as ur_add_views
    ur_add_views(sys_admin)

    # collect views and initiate resources
    global all_views
    all_views = getattr(sys_admin, '_views', [])


def collect_views():
    """自动添加 Views 到 Resource表，并赋给admin用户"""
    from app.models import Resource, Role
    from app import db

    view_list = []

    for view in all_views:
        if hasattr(view, 'get_model_name'):
            view_name = view.get_model_name()
            if view_name is not None:
                view_list.append(view_name)

    view_list.append('FileUpload')  # 文件上传用

    if len(view_list) > 0:
        __role_changed = False
        role = Role.query.filter_by(role_code='ADMIN').first()
        if role is None:
            role = Role(role_code='ADMIN', role_name='系统管理员')
            __role_changed = True

        for v in view_list:
            res = Resource.query.filter_by(resource_code=v, resource_type='VIEW').first()
            if res is None:
                res = Resource(resource_code=v, resource_name=v, resource_type='VIEW')
                """反向添加resource 到 <Role ADMIN>下："""
                role.resources.append(res)
                __role_changed = True

        if __role_changed:
            db.session.add(role)
            db.session.commit()

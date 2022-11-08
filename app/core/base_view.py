import abc
import logging
from datetime import date
from flask_login import current_user
from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from flask_admin import expose

logger = logging.getLogger()


def datetime_format(view, value):
    return value.strftime('%Y-%m-%d %H:%M:%S')


def date_format(view, value):
    return value.strftime('%Y-%m-%d')


DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
DEFAULT_FORMATTERS.update({
    date: datetime_format,
})


# Views
class CommonView(ModelView):
    page_size = 50
    can_view_details = True
    can_delete = False
    action_disallowed_list = ['delete']
    column_type_formatters = DEFAULT_FORMATTERS
    form_excluded_columns = ['created_at', 'updated_at']
    can_delete_in_detail = False
    edit_template = 'admin/model/my_edit.html'
    list_template = 'admin/model/my_list.html'
    extra_css = []
    menu_icon_type = 'glyph'

    def get_model_name(self):
        if self.model is not None:
            return self.model.__name__
        else:
            return None

    def is_accessible(self):
        """当用户具有模块/菜单权限时，才允许访问"""
        curr_model_name = self.get_model_name()
        # print(current_user, login_manager.user_unauthorized)
        """加载用户资源列表，判断当前用户是否有此模块的权限。用户资源列表应该缓存 TODO """
        if not current_user or current_user.is_anonymous:
            return False
        else:
            res = current_user.get_resources()
            # print(res, curr_model_name)
            if res is not None and type(res) is list and curr_model_name in res:
                return True

        return False

    def inaccessible_callback(self, name, **kwargs):
        """无访问权限时的回调函数：跳转登录页面"""
        return redirect(url_for('auth.login', next=request.url))

    @expose('/delete/<id>', methods=('GET',))
    def del_by_id(self, id):
        print('deleting', self.get_model_name(), 'by id:', id)
        model = self.get_one(id)
        if self.delete_model(model):
            flash('已删除！', 'success')

        return redirect(url_for('.index_view'))


class BaseView(CommonView):
    @abc.abstractmethod
    def row_attributes(self, obj):
        pass

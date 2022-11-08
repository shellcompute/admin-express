from sqlalchemy.exc import SQLAlchemyError
from wtforms.validators import input_required as required, ValidationError
from flask_admin.model.form import InlineFormAdmin
from flask_admin.contrib.sqla.form import InlineModelConverter
from flask_admin.contrib.sqla.fields import InlineModelFormList
from app.core import CommonView
from app import db
from app.models import Role, Resource
from config import USER_AUDIT_ENABLED


# class ResourceInlineModelForm(InlineFormAdmin):
#     form_columns = ('resource_code', 'resource_name')


class ResourceHiddenModelFormList(InlineModelFormList):
    def display_row_controls(self, field):
        return False


class ResourceInlineModelConverter(InlineModelConverter):
    inline_field_list_type = ResourceHiddenModelFormList


class RoleView(CommonView):
    column_display_actions = True
    column_searchable_list = None
    column_list = ('id', 'role_code', 'role_name', 'created_at')
    column_labels = {
        'role_code': '角色代码',
        'role_name': '角色名称',
        'created_at': '创建时间',
    }
    column_sortable_list = ('id', 'role_code')
    column_default_sort = ('id', True)
    column_filters = ('created_at', 'role_code')

    form_columns = ('role_code', 'role_name', 'resources')

    form_args = {
        'role_code': {
            'validators': [required()],
        },
        'role_name': {
            'validators': [required()],
        },
    }

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
    }

    # inline_model_form_converter = ResourceInlineModelConverter

    # inline_models = [(ResourceInlineModelForm(Resource),)]
    # inline_models = [(Resource, {
    #     'form_label': '资源',
    #     'form_columns': ['resource_name', 'id'],
    #     'column_labels': {
    #         'resource_name': '资源名称'
    #     },
    #     'form_widget_args': {
    #         'resource_name': {'readonly': True},
    #     }
    # })]


class ResourceView(CommonView):
    column_display_actions = True
    column_searchable_list = None
    column_list = ('id', 'resource_code', 'resource_name', 'resource_type', 'parent_id', 'url', 'created_at')
    column_labels = {
        'id': 'ID',
        'resource_code': '资源代码',
        'resource_name': '资源名称',
        'resource_type': '资源类型',
        'parent_id': '上级资源ID',
        'url': 'URL',
        'created_at': '创建时间'
    }
    column_sortable_list = ('id', 'resource_code')
    column_default_sort = ('id', True)

    column_filters = ('created_at', 'resource_code')
    form_columns = ('resource_code', 'resource_name', 'resource_type', 'parent_id', 'url', 'created_at')

    column_choices = {
        'resource_type': [
            ('VIEW', '页面视图'),
            ('LINK', '页面链接'),
        ]
    }

    form_choices = column_choices

    form_args = {
        'resource_code': {
            'label': '资源代码',
            'validators': [required()],
        },
        'resource_name': {
            'label': '资源名称',
            'validators': [required()],
        },
    }

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
    }


class UserView(CommonView):
    can_create = False
    can_delete = False
    column_display_actions = True
    column_searchable_list = None
    column_list = ('id', 'username', 'realname', 'activated', 'email', 'mobile', 'created_at')
    column_labels = {
        'id': 'ID',
        'username': '用户账号',
        'realname': '真实姓名',
        'activated': '是否已激活',
        'email': 'Email',
        'mobile': '手机号码',
        'created_at': '创建时间',
        'roles': '角色'
    }
    column_sortable_list = ('id', 'username')
    column_default_sort = ('id', True)
    column_choices = {
        'activated': [
            ('1', '是'),
            ('A', '待审核'),
            ('0', '否'),
        ]
    }

    column_filters = ('username', 'realname', 'created_at')

    form_columns = ('username', 'realname', 'activated', 'email', 'mobile', 'created_at', 'roles')

    if USER_AUDIT_ENABLED:
        form_choices = {
            'activated': [
                ('1', '是'),
                ('A', '待审核'),
                ('0', '否'),
            ]
        }
    else:
        form_choices = {
            'activated': [
                ('1', '是'),
                ('0', '否'),
            ]
        }

    form_args = {
        'username': {
            'validators': [required()],
        },
        'realname': {
            'validators': [required()],
        }
    }

    form_widget_args = {
        'created_at': {
            'disabled': True
        },
    }

    # inline_models = [(Role, {
    #     'form_label': '角色',
    #     # 'form_columns': ['role_name'],
    #     'form_excluded_columns': ['created_at', 'updated_at', 'resources', 'role_code'],
    #     'form_widget_args': {
    #         'role_name': {'readonly': True}
    #     }
    # })]

    def on_model_change(self, form, model, is_created):
        if not is_created:
            """当修改时"""
            print(form.username.data)



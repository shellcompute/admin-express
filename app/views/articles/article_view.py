from datetime import datetime
from wtforms.validators import input_required as required
from app.core import CommonView
from app import db
from app.models import User
from flask_login import current_user


class ArticleView(CommonView):
    column_display_actions = True
    column_searchable_list = ['title']
    column_list = ('title', 'content', 'tags', 'created_by', 'created_at', )
    column_labels = {
        'id': 'ID',
        'title': '标题',
        'content': '内容',
        'tags': '标签',
        'created_at': '创建时间',
        'updated_at': '最近修改时间',
        'created_by': '作者',
        'updated_by': '修改人'
    }
    column_sortable_list = ('created_at', 'title')
    column_default_sort = ('created_at', True)

    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%Y-%m-%d %H:%M') if m.created_at is not None else '',
        'updated_at': lambda v, c, m, p: m.updated_at.strftime('%Y-%m-%d %H:%M') if m.updated_at is not None else ''
    }

    column_filters = ('created_by', 'title')
    form_columns = ('title', 'content', 'tags', 'created_by', 'created_at')

    column_choices = {
        # 'resource_type': [
        #     ('VIEW', '页面视图'),
        #     ('LINK', '页面链接'),
        # ]
    }

    form_choices = column_choices

    form_args = {
        'title': {
            'label': '标题',
            'validators': [required()],
        },
        'content': {
            'label': '正文',
            'validators': [required()],
        },
    }

    form_widget_args = {
        'content': {
            'rows': 20,
            'style': 'color: black'
        },
        'created_at': {
            'disabled': True
        },
        'created_by': {
            'disabled': True
        }
    }

    def on_form_prefill(self, form, id):
        """编辑时，设置字段只读"""
        form.created_by.render_kw = {'disabled': True}
        form.created_at.render_kw = {'disabled': True}

    def after_model_change(self, form, model, is_created):
        """当模型保存时，添加创建人/修改人等信息"""
        user_id = current_user.get_id()
        user = User.query.filter_by(id=user_id).first()
        if is_created:
            model.created_by = user.username
            model.updated_by = user.username
        else:
            model.updated_by = user.username
            model.updated_at = datetime.now()

        db.session.commit()

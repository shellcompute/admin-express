from flask_admin import BaseView, expose, babel


class HomeView(BaseView):
    """自定义主页视图"""

    def __init__(self, name=None, category=None,
                 endpoint=None, url=None,
                 template='index3.html',
                 menu_class_name=None,
                 menu_icon_type='glyph',
                 menu_icon_value='glyphicon-home'):
        super().__init__(name or babel.lazy_gettext('Home'),
                         category,
                         endpoint or 'admin',
                         '/admin' if url is None else url,
                         static_folder='static',
                         static_url_path='/static',
                         menu_class_name=menu_class_name,
                         menu_icon_type=menu_icon_type,
                         menu_icon_value=menu_icon_value)
        self.extra_js = ['js/index3.js']
        self.extra_css = []
        self._template = template

    @expose()
    def index(self):
        return self.render(self._template)

    def get_model_name(self):
        return None

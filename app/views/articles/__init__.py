from app.models import Article
from app import db
from .article_view import ArticleView


def add_views(sys_admin):
    sys_admin.add_view(ArticleView(Article, db.session, name="文章管理", menu_icon_type='glyph', menu_icon_value='glyphicon-book'))


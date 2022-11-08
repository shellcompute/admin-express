from sqlalchemy import ForeignKey, UniqueConstraint, Column
from sqlalchemy.sql.sqltypes import String, Integer, Date, Text
from app.core.base_model import BaseModel


class Article(BaseModel):
    __tablename__ = 't_article'
    title = Column(String(64))
    content = Column(Text, nullable=False)
    tags = Column(String(64), nullable=True)

    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

    def __repr__(self):
        return '<Art %s>' % self.id

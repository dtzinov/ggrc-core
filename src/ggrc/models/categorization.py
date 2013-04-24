from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base

class Categorization(Base, db.Model):
  __tablename__ = 'categorizations'

  category_id = db.Column(
      db.Integer, db.ForeignKey('categories.id'))
  categorizable_id = db.Column(db.Integer)
  categorizable_type = db.Column(db.String)

  @property
  def categorizable_attr(self):
    return '{}_categorizable'.format(self.categorizable_type)

  @property
  def categorizable(self):
    return getattr(self, self.categorizable_attr)

  @categorizable.setter
  def categorizable(self, value):
    setattr(self, self.categorizable_attr, value)

class Categorizable(object):
  @declared_attr
  def categorizations(cls):
    cls.categories = association_proxy(
        'categorizations', 'category',
        creator=lambda category: Categorization(
            category=category,
            #FIXME add from http session!
            modified_by_id=1,
            categorizable_type=cls.__name__,
            ),
        )
    joinstr = 'and_(foreign(Categorization.categorizable_id) == {type}.id, '\
                   'foreign(Categorization.categorizable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'Categorization',
        primaryjoin=joinstr,
        backref='{}_categorizable'.format(cls.__name__),
        )

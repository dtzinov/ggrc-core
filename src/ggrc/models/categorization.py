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
    return '{}_{}_categorizable'.format(
        self.categorizable_type, self.category.scope_id)

  @property
  def categorizable(self):
    return getattr(self, self.categorizable_attr)

  @categorizable.setter
  def categorizable(self, value):
    setattr(self, self.categorizable_attr, value)

class Categorizable(object):
  '''Subclasses **MUST** provide a declared_attr method that defines the
  relationship and association_proxy. For example:
    
  ..
     
     @declared_attr
     def control_categorizations(cls):
       return cls.categorizations(
           'control_categorizations', 'control_categories', 100)
  '''
  @classmethod
  def _categorizations(cls, rel_name, proxy_name, scope):
    setattr(cls, proxy_name, association_proxy(
        rel_name, 'category',
        creator=lambda category: Categorization(
            category=category,
            #FIXME add from http session!
            modified_by_id=1,
            categorizable_type=cls.__name__,
            ),
        ))
    joinstr = 'and_(foreign(Categorization.categorizable_id) == {type}.id, '\
                   'foreign(Categorization.categorizable_type) == "{type}", '\
                   'Categorization.category_id == Category.id, '\
                   'Category.scope_id == {scope})'
    joinstr = joinstr.format(type=cls.__name__, scope=scope)
    return db.relationship(
        'Categorization',
        primaryjoin=joinstr,
        backref='{}_{}_categorizable'.format(cls.__name__, scope),
        )

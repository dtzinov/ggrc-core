
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from .mixins import Base

BACKREF_NAME_FORMAT = '{type}_{scope}_categorizable'

class Categorization(Base, db.Model):
  __tablename__ = 'categorizations'

  category_id = db.Column(
      db.Integer, db.ForeignKey('categories.id'))
  categorizable_id = db.Column(db.Integer)
  categorizable_type = db.Column(db.String)

  @property
  def categorizable_attr(self):
    return BACKREF_NAME_FORMAT.format(
        type=self.categorizable_type, scope=self.category.scope_id)

  @property
  def categorizable(self):
    return getattr(self, self.categorizable_attr)

  @categorizable.setter
  def categorizable(self, value):
    setattr(self, self.categorizable_attr, value)

  _publish_attrs = [
      'categorizable',
      'category',
      ]
  _update_attrs = []

class Categorizable(object):
  """Subclasses **MUST** provide a declared_attr method that defines the
  relationship and association_proxy. For example:
    
  ..
     
     @declared_attr
     def control_categorizations(cls):
       return cls.categorizations(
           'control_categorizations', 'control_categories', 100)
  """
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
        backref=BACKREF_NAME_FORMAT.format(type=cls.__name__, scope=scope),
        )

  # FIXME: make eager-loading work for categorizations/assertations
  #@classmethod
  #def eager_query(cls):
  #  from sqlalchemy import orm

  #  query = super(Categorizable, cls).eager_query()
  #  return query.options(
  #      orm.subqueryload_all('categorizations.category'),
  #      orm.subqueryload_all('assertations.category'))
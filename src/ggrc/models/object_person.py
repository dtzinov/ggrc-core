
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base, Timeboxed
from .reflection import PublishOnly

class ObjectPerson(Base, Timeboxed, db.Model):
  __tablename__ = 'object_people'

  role = db.Column(db.String)
  notes = db.Column(db.Text)
  person_id = db.Column(db.Integer, db.ForeignKey('people.id'))

  # TODO: Polymorphic relationship
  personable_id = db.Column(db.Integer)
  personable_type = db.Column(db.String)

  @property
  def personable_attr(self):
    return '{0}_personable'.format(self.personable_type)

  @property
  def personable(self):
    return getattr(self, self.personable_attr)

  @personable.setter
  def personable(self, value):
    self.personable_id = value.id if value is not None else None
    self.personable_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.personable_attr, value)

  _publish_attrs = [
      'role',
      'notes',
      'person',
      'personable',
      ]

class Personable(object):
  @declared_attr
  def object_people(cls):
    cls.people = association_proxy(
        'object_people', 'person',
        creator=lambda person: ObjectPerson(
            person=person,
            modified_by_id=1,
            personable_type=cls.__name__,
            )
        )
    joinstr = 'and_(foreign(ObjectPerson.personable_id) == {type}.id, '\
                   'foreign(ObjectPerson.personable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'ObjectPerson',
        primaryjoin=joinstr,
        backref='{0}_personable'.format(cls.__name__),
        )

  _publish_attrs = [
      PublishOnly('people'),
      'object_people',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Personable, cls).eager_query()
    return query.options(orm.subqueryload_all('object_people.person'))

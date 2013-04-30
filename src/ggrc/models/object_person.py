from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base, Timeboxed

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
    return '{}_personable'.format(self.personable_type)

  @property
  def personable(self):
    return getattr(self, self.personable_attr)

  @personable.setter
  def personable(self, value):
    setattr(self, self.personable_attr, value)

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
        backref='{}_personable'.format(cls.__name__),
        )

  _publish_attrs = [
      'people',
      'object_people',
      ]
  _update_attrs = []

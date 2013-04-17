from ggrc import db
from .mixins import Base, Timeboxed

class ObjectPerson(Base, Timeboxed, db.Model):
  __tablename__ = 'object_people'

  role = db.Column(db.String)
  notes = db.Column(db.Text)
  person_id = db.Column(db.Integer, db.ForeignKey('people.id'))

  # TODO: Polymorphic relationship
  personable_id = db.Column(db.Integer)
  personable_type = db.Column(db.String)

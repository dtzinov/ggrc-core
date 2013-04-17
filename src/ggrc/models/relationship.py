from ggrc import db
from .mixins import Base

class Relationship(Base, db.Model):
  __tablename__ = 'relationships'

  #TODO: Polymorphic association
  source_id = db.Column(db.Integer)
  source_type = db.Column(db.String)

  destination_id = db.Column(db.Integer)
  destination_type = db.Column(db.String)

  # TODO: Foreign key into RelationshipType?
  relationship_type_id = db.Column(db.String)

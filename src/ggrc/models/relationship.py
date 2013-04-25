import ggrc.models
from ggrc import db
from .mixins import Base, Described

class Relationship(Base, db.Model):
  __tablename__ = 'relationships'
  source_id = db.Column(db.Integer)
  source_type = db.Column(db.String)
  destination_id = db.Column(db.Integer)
  destination_type = db.Column(db.String)
  relationship_type_id = db.Column(
      db.Integer, db.ForeignKey('relationship_types.id'))
  relationship_type = db.relationship('RelationshipType', uselist=False)

  def get_relationship_node(self, attr, node_type, node_id):
    if hasattr(self, attr):
      return getattr(self, attr)
    cls = getattr(ggrc.models, node_type)
    value = db.session.query(cls).get(self.node_id)
    setattr(self, attr, value)
    return value

  #FIXME This provides access to source and destination, but likely breaks some
  #notification semantics in sqlalchemy. Is it necessary to go beyond this,
  #though? Are there motivating use cases??

  @property
  def source(self):
    return self.get_relationship_node(
        '_source', self.source_type, self.source_id)

  @source.setter
  def source(self, value):
    setattr(self, '_source', value)
    self.source_id = value.id
    self.source_type = value.__class__.name

  @property
  def destination(self):
    return self.get_relationship_node(
        '_destination', self.destination_type, self.destination_id)

  @destination.setter
  def destination(self, value):
    setattr(self, '_destination', value)
    self.destination_id = value.id
    self.destination_type = value.__class__.name

class RelationshipType(Base, Described, db.Model):
  __tablename__ = 'relationship_types'
  forward_phrase = db.Column(db.String)
  backward_phrase = db.Column(db.String)
  symmetric = db.Column(db.Boolean, nullable=False)

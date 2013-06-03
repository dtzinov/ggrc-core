
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

import ggrc.models
from ggrc import db
from .mixins import Base, Described

class Relationship(Base, db.Model):
  __tablename__ = 'relationships'
  source_id = db.Column(db.Integer)
  source_type = db.Column(db.String)
  destination_id = db.Column(db.Integer)
  destination_type = db.Column(db.String)
  relationship_type_id = db.Column(db.String)
  # FIXME: Should this be a strict constraint?  If so, a migration is needed.
  #relationship_type_id = db.Column(
  #    db.Integer, db.ForeignKey('relationship_types.id'))
  relationship_type = db.relationship(
      'RelationshipType',
      primaryjoin='foreign(RelationshipType.relationship_type) == Relationship.relationship_type_id',
      uselist=False)

  def get_relationship_node(self, attr, node_type, node_id):
    if hasattr(self, attr):
      return getattr(self, attr)
    if node_type is None:
      return None
    cls = getattr(ggrc.models, node_type)
    value = db.session.query(cls).get(node_id)
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
    self.source_id = value.id if value is not None else None
    self.source_type = value.__class__.__name__ if value is not None else None

  @property
  def destination(self):
    return self.get_relationship_node(
        '_destination', self.destination_type, self.destination_id)

  @destination.setter
  def destination(self, value):
    setattr(self, '_destination', value)
    self.destination_id = value.id if value is not None else None
    self.destination_type = value.__class__.__name__ if value is not None \
        else None

  _publish_attrs = [
      'source',
      'destination',
      'relationship_type_id',
      ]

class RelationshipType(Base, Described, db.Model):
  __tablename__ = 'relationship_types'
  relationship_type = db.Column(db.String)
  forward_phrase = db.Column(db.String)
  backward_phrase = db.Column(db.String)
  symmetric = db.Column(db.Boolean, nullable=False)

  _publish_attrs = [
      'forward_phrase',
      'backward_phrase',
      'symmetric',
      ]
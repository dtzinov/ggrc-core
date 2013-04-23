from ggrc import db
from .mixins import Slugged, Described, Hierarchical, Hyperlinked, Timeboxed

class Control(Slugged, Described, Hierarchical, Hyperlinked, Timeboxed, db.Model):
  __tablename__ = 'controls'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  type_id = db.Column(db.Integer)
  kind_id = db.Column(db.Integer)
  means_id = db.Column(db.Integer)
  version = db.Column(db.String)
  documentation_description = db.Column(db.Text)
  verify_frequency_id = db.Column(db.Integer)
  fraud_related = db.Column(db.Boolean)
  key_control = db.Column(db.Boolean)
  active = db.Column(db.Boolean)
  notes = db.Column(db.Text)

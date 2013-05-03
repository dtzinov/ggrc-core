from ggrc import db
from .mixins import Base

class ControlAssessment(Base, db.Model):
  __tablename__ = 'control_assessments'

  pbc_list_id = db.Column(db.Integer, db.ForeignKey('pbc_lists.id'))
  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  control_version = db.Column(db.String)
  internal_tod = db.Column(db.Boolean)
  internal_toe = db.Column(db.Boolean)
  external_tod = db.Column(db.Boolean)
  external_toe = db.Column(db.Boolean)
  notes = db.Column(db.Text)
  requests = db.relationship('Request', backref='control_assessment')

  _publish_attrs = [
      'pbc_list',
      'control',
      'control_version',
      'internal_tod',
      'internal_toe',
      'external_tod',
      'external_toe',
      'notes',
      'requests',
      ]

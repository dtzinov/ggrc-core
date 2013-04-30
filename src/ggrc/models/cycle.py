from ggrc import db
from .mixins import Base, Described

class Cycle(Base, Described, db.Model):
  __tablename__ = 'cycles'

  start_at = db.Column(db.Date)
  complete = db.Column(db.Boolean, default=False, nullable=False)
  title = db.Column(db.String)
  audit_firm = db.Column(db.String)
  audit_lead = db.Column(db.String)
  status = db.Column(db.String)
  notes = db.Column(db.Text)
  end_at = db.Column(db.Date)
  program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
  report_due_at = db.Column(db.Date)
  pbc_lists = db.relationship('PbcList', backref='audit_cycle')

  _publish_attrs = [
      'start_at',
      'complete',
      'title',
      'audit_firm',
      'audit_lead',
      'status',
      'notes',
      'end_at',
      'program',
      'report_due_at',
      'pbc_lists',
      ]
  _update_attrs = [
      'start_at',
      'complete',
      'title',
      'audit_firm',
      'audit_lead',
      'status',
      'notes',
      'end_at',
      'report_due_at',
      ]


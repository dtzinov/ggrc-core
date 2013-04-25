from ggrc import db
from .mixins import Base

class PbcList(Base, db.Model):
  __tablename__ = 'pbc_lists'

  audit_cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))
  requests = db.relationship('Request', backref='pbc_list')
  control_assessments = db.relationship('ControlAssessment', backref='pbc_list')

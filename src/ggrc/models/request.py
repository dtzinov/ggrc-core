from ggrc import db
from .mixins import Base

class Request(Base, db.Model):
  __tablename__ = 'requests'

  pbc_list_id = db.Column(db.Integer, db.ForeignKey('pbc_lists.id'))
  type_id = db.Column(db.Integer)
  pbc_control_code = db.Column(db.String)
  pbc_control_desc = db.Column(db.Text)
  request = db.Column(db.Text)
  test = db.Column(db.Text)
  notes = db.Column(db.Text)
  company_responsible = db.Column(db.String)
  auditor_responsible = db.Column(db.String)
  date_requested = db.Column(db.DateTime)
  status = db.Column(db.String)
  control_assessment_id = db.Column(db.Integer, db.ForeignKey('control_assessments.id'))
  response_due_at = db.Column(db.Date)

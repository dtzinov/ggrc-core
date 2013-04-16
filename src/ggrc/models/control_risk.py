from ggrc import db
from .mixins import Base

class ControlRisk(Base, db.Model):
  __tablename__ = 'control_risks'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  risk_id = db.Column(db.Integer, db.ForeignKey('risks.id'))

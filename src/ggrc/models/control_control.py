from ggrc import db
from .mixins import Base

class ControlControl(Base, db.Model):
  __tablename__ = 'control_controls'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  implemented_control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))

from ggrc import db
from .mixins import Base

class SystemControl(Base, db.Model):
  __tablename__ = 'system_controls'

  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))

  state = db.Column(db.Integer, default=1, nullable=False)
  cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))

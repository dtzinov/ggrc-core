from ggrc import db
from .mixins import Base

class SystemSystem(Base, db.Model):
  __tablename__ = 'system_systems'

  parent_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  child_id = db.Column(db.Integer, db.ForeignKey('systems.id'))

  type = db.Column(db.String)
  order = db.Column(db.Integer)

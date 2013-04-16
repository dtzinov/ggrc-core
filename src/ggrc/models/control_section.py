from ggrc import db
from .mixins import Base

class ControlSection(Base, db.Model):
  __tablename__ = 'control_sections'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

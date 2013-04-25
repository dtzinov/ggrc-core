from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from .mixins import BusinessObject, Hierarchical

class Section(Hierarchical, BusinessObject, db.Model):
  __tablename__ = 'sections'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  na = db.Column(db.Boolean, default=False, nullable=False)
  notes = db.Column(db.Text)
  control_sections = db.relationship('ControlSection', backref='section')
  controls = association_proxy('control_sections', 'control')

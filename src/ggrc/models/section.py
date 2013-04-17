from ggrc import db
from .mixins import BusinessObject, Child

class Section(BusinessObject, Child, db.Model):
  __tablename__ = 'sections'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  na = db.Column(db.Boolean, default=False, nullable=False)
  notes = db.Column(db.Text)

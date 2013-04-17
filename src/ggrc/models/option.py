from ggrc import db
from .mixins import Base, Described

class Option(Base, Described, db.Model):
  __tablename__ = 'options'

  role = db.Column(db.String)
  title = db.Column(db.String)
  required = db.Column(db.Boolean)

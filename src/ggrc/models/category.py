from ggrc import db
from .mixins import Base, Hierarchical

class Category(Base, Hierarchical, db.Model):
  __tablename__ = 'categories'

  name = db.Column(db.String)
  lft = db.Column(db.Integer)
  rgt = db.Column(db.Integer)
  scope_id = db.Column(db.Integer)
  depth = db.Column(db.Integer)
  required = db.Column(db.Boolean)

from ggrc import db
from sqlalchemy import Boolean, Column, DateTime, Integer, String

class Category(db.Model):
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  parent_id = db.Column(db.Integer)
  lft = db.Column(db.Integer)
  rgt = db.Column(db.Integer)
  scope_id = db.Column(db.Integer)
  depth = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)
  modified_by_id = db.Column(db.Integer)
  required = db.Column(db.Boolean)


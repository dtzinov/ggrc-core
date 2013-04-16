from ggrc import db

class Category(db.Model):
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  parent_id = db.Column(db.Integer)
  lft = db.Column(db.Integer)
  rgt = db.Column(db.Integer)
  scope_id = db.Column(db.Integer)
  depth = db.Column(db.Integer)
  created_at = db.Column(db.DateTime, server_default=db.text('current_timestamp'))
  updated_at = db.Column(db.DateTime, server_onupdate=db.text('current_timestamp'))
  modified_by_id = db.Column(db.Integer)
  required = db.Column(db.Boolean)


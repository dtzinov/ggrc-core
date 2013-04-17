from ggrc import db
from .mixins import Identifiable

class Version(Identifiable, db.Model):
  __tablename__ = 'versions'

  item_type = db.Column(db.String)
  item_id = db.Column(db.Integer)
  event = db.Column(db.String)
  whodunnit = db.Column(db.String)
  object = db.Column(db.Text)
  created_at = db.Column(db.DateTime)

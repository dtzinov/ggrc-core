from ggrc import db
from .mixins import Base

class Document(Base, db.Model):
  __tablename__ = 'documents'

  title = db.Column(db.String)
  link = db.Column(db.String)
  description = db.Column(db.Text)
  type_id = db.Column(db.Integer)
  kind_id = db.Column(db.Integer)
  year_id = db.Column(db.Integer)
  language_id = db.Column(db.Integer)

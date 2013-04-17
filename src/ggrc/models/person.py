from ggrc import db
from .mixins import Base

class Person(Base, db.Model):
  __tablename__ = 'people'

  email = db.Column(db.String)
  name = db.Column(db.String)
  language_id = db.Column(db.Integer)
  company = db.Column(db.String)

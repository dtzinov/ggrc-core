from ggrc import db
from .mixins import BusinessObject

class Program(BusinessObject, db.Model):
  __tablename__ = 'programs'

  kind = db.Column(db.String)

from ggrc import db
from .mixins import BusinessObject

class RiskyAttribute(BusinessObject, db.Model):
  __tablename__ = 'risky_attributes'

  type_string = db.Column(db.String)

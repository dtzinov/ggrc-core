from ggrc import db
from .mixins import BusinessObject

class Product(BusinessObject, db.Model):
  __tablename__ = 'products'

  type_id = db.Column(db.Integer)
  version = db.Column(db.String)

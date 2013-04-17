from ggrc import db
from .mixins import BusinessObject

class Facility(BusinessObject, db.Model):
  __tablename__ = 'facilities'

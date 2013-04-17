from ggrc import db
from .mixins import BusinessObject

class Market(BusinessObject, db.Model):
  __tablename__ = 'markets'

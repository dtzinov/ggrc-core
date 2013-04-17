from ggrc import db
from .mixins import BusinessObject

class DataAsset(BusinessObject, db.Model):
  __tablename__ = 'data_assets'

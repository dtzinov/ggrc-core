from ggrc import db
from .mixins import BusinessObject
from .object_document import Documentable
from .object_person import Personable

class DataAsset(Personable, Documentable, BusinessObject, db.Model):
  __tablename__ = 'data_assets'

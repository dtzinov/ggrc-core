from ggrc import db
from .mixins import BusinessObject

class Project(BusinessObject, db.Model):
  __tablename__ = 'projects'

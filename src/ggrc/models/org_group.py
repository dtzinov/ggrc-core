from ggrc import db
from .mixins import BusinessObject

class OrgGroup(BusinessObject, db.Model):
  __tablename__ = 'org_groups'

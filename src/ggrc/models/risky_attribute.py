from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from .mixins import BusinessObject
from .object_document import Documentable
from .object_person import Personable

class RiskyAttribute(Documentable, Personable, BusinessObject, db.Model):
  __tablename__ = 'risky_attributes'

  type_string = db.Column(db.String)
  risk_risky_attributes = db.relationship(
      'RiskRiskyAttribute', backref='risky_attribute')
  risks = association_proxy('risk_risky_attributes', 'risk')

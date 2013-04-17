from ggrc import db
from .mixins import Base

class RiskRiskyAttribute(Base, db.Model):
  __tablename__ = 'risk_risky_attributes'

  risk_id = db.Column(db.Integer, db.ForeignKey('risks.id'))
  risky_attribute_id = db.Column(db.Integer, db.ForeignKey('risky_attributes.id'))

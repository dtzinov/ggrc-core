from ggrc import db
from .associationproxy import association_proxy
from .control import ControlCategorized
from .mixins import BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

class Risk(
    Documentable, Personable, Timeboxed, BusinessObject, ControlCategorized , db.Model):
  __tablename__ = 'risks'

  kind = db.Column(db.String)
  likelihood = db.Column(db.Text)
  threat_vector = db.Column(db.Text)
  trigger = db.Column(db.Text)
  preconditions = db.Column(db.Text)

  likelihood_rating = db.Column(db.Integer)
  financial_impact_rating = db.Column(db.Integer)
  reputational_impact_rating = db.Column(db.Integer)
  operational_impact_rating = db.Column(db.Integer)

  inherent_risk = db.Column(db.Text)
  risk_mitigation = db.Column(db.Text)
  residual_risk = db.Column(db.Text)
  impact = db.Column(db.Text)
  control_risks = db.relationship('ControlRisk', backref='risk')
  controls = association_proxy('control_risks', 'control', 'ControlRisk')
  risk_risky_attributes = db.relationship(
      'RiskRiskyAttribute', backref='risk')
  risky_attributes = association_proxy(
      'risk_risky_attributes', 'risky_attribute', 'RiskRiskyAttribute')

  _publish_attrs = [
      'kind',
      'likelihood',
      'threat_vector',
      'trigger',
      'preconditions',
      'likelihood_rating',
      'financial_impact_rating',
      'reputational_impact_rating',
      'operational_impact_rating',
      'inherent_risk',
      'residual_risk',
      'impact',
      PublishOnly('control_risks'),
      'controls',
      PublishOnly('risk_risky_attributes'),
      'risky_attributes',
      ]

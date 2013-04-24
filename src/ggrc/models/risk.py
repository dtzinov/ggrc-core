from ggrc import db
from .categorization import Categorizable
from .mixins import BusinessObject

class Risk(BusinessObject, Categorizable, db.Model):
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

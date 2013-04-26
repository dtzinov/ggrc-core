from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .categorization import Categorizable
from .mixins import Slugged, Described, Hierarchical, Hyperlinked, Timeboxed
from .object_document import Documentable
from .object_person import Personable

CATEGORY_CONTROL_TYPE_ID = 100
CATEGORY_ASSERTION_TYPE_ID = 102

class ControlCategorized(Categorizable):
  @declared_attr
  def categorizations(cls):
    return cls._categorizations(
        'categorizations', 'categories', CATEGORY_CONTROL_TYPE_ID)

class AssertionCategorized(Categorizable):
  @declared_attr
  def assertations(cls):
    return cls._categorizations(
        'assertations', 'assertions', CATEGORY_ASSERTION_TYPE_ID)

class Control(
    Documentable, Personable, ControlCategorized, AssertionCategorized,
    Slugged, Described, Hierarchical, Hyperlinked, Timeboxed, db.Model):
  __tablename__ = 'controls'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  type_id = db.Column(db.Integer)
  kind_id = db.Column(db.Integer)
  means_id = db.Column(db.Integer)
  version = db.Column(db.String)
  documentation_description = db.Column(db.Text)
  verify_frequency_id = db.Column(db.Integer)
  fraud_related = db.Column(db.Boolean)
  key_control = db.Column(db.Boolean)
  active = db.Column(db.Boolean)
  notes = db.Column(db.Text)
  system_controls = db.relationship('SystemControl', backref='control')
  systems = association_proxy('system_controls', 'system')
  control_sections = db.relationship('ControlSection', backref='control')
  sections = association_proxy('control_sections', 'section')
  control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.control_id',
      backref='control',
      )
  implemented_controls = association_proxy(
      'control_controls', 'implemented_control')
  implementing_control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.implemented_control_id',
      backref='implemented_control',
      )
  implementing_controls = association_proxy(
      'implementing_control_controls', 'control')
  control_risks = db.relationship('ControlRisk', backref='control')
  risks = association_proxy('control_risks', 'risk')
  control_assessments = db.relationship('ControlAssessment', backref='control')

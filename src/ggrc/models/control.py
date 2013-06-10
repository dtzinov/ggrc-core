# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from sqlalchemy.ext.declarative import declared_attr
from .associationproxy import association_proxy
from .categorization import Categorizable
from .mixins import Slugged, Described, Hierarchical, Hyperlinked, Timeboxed
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

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
    Described, Hierarchical, Hyperlinked, Timeboxed, Slugged, db.Model):
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
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.type_id) == Option.id, '\
                  'Option.role == "control_type")',
      uselist=False)
  kind = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.kind_id) == Option.id, '\
                  'Option.role == "control_kind")',
      uselist=False)
  means = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.means_id) == Option.id, '\
                  'Option.role == "control_means")',
      uselist=False)
  verify_frequency = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Control.verify_frequency_id) == Option.id, '\
                  'Option.role == "verify_frequency")',
      uselist=False)
  system_controls = db.relationship('SystemControl', backref='control')
  systems = association_proxy('system_controls', 'system', 'SystemControl')
  control_sections = db.relationship('ControlSection', backref='control')
  sections = association_proxy('control_sections', 'section', 'ControlSection')
  control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.control_id',
      backref='control',
      )
  implemented_controls = association_proxy(
      'control_controls', 'implemented_control', 'ControlControl')
  implementing_control_controls = db.relationship(
      'ControlControl',
      foreign_keys='ControlControl.implemented_control_id',
      backref='implemented_control',
      )
  implementing_controls = association_proxy(
      'implementing_control_controls', 'control', 'ControlControl')
  control_risks = db.relationship('ControlRisk', backref='control')
  risks = association_proxy('control_risks', 'risk', 'ControlRisk')
  control_assessments = db.relationship('ControlAssessment', backref='control')

  # REST properties
  _publish_attrs = [
      'active',
      # FIXME: add these in once eager-loading works correctly
      #'categories',
      #'assertions',
      'control_assessments',
      'directive',
      'documentation_description',
      'fraud_related',
      'implemented_controls',
      'implementing_controls',
      'key_control',
      'kind',
      'means',
      'notes',
      'risks',
      'sections',
      'systems',
      'type',
      'verify_frequency',
      'version',
      PublishOnly('control_controls'),
      PublishOnly('control_risks'),
      PublishOnly('control_sections'),
      PublishOnly('implementing_control_controls'),
      PublishOnly('system_controls'),
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Control, cls).eager_query()
    return query.options(
        orm.joinedload('directive'),
        orm.joinedload('type'),
        orm.joinedload('kind'),
        orm.joinedload('means'),
        orm.joinedload('verify_frequency'),
        orm.subqueryload_all('system_controls.system'),
        orm.subqueryload_all('control_sections.section'),
        orm.subqueryload_all('control_controls.implemented_control'),
        orm.subqueryload_all('implementing_control_controls.control'),
        orm.subqueryload_all('control_risks.risk'),
        orm.subqueryload_all('control_assessments'))

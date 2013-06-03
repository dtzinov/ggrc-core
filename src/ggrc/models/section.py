
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, Hierarchical

class Section(Hierarchical, BusinessObject, db.Model):
  __tablename__ = 'sections'

  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))
  na = db.Column(db.Boolean, default=False, nullable=False)
  notes = db.Column(db.Text)
  control_sections = db.relationship('ControlSection', backref='section')
  controls = association_proxy('control_sections', 'control', 'ControlSection')

  _publish_attrs = [
      'directive',
      'na',
      'notes',
      'control_sections',
      'controls',
      ]
  _update_attrs = [
      'directive',
      'na',
      'notes',
      'controls',
      ]
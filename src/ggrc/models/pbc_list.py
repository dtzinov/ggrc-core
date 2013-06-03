
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class PbcList(Base, db.Model):
  __tablename__ = 'pbc_lists'

  audit_cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))
  requests = db.relationship('Request', backref='pbc_list')
  control_assessments = db.relationship('ControlAssessment', backref='pbc_list')

  _publish_attrs = [
      'audit_cycle',
      'requests',
      'control_assessments',
      ]
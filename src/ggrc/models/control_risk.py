
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class ControlRisk(Base, db.Model):
  __tablename__ = 'control_risks'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  risk_id = db.Column(db.Integer, db.ForeignKey('risks.id'))

  _publish_attrs = [
      'control',
      'risk',
      ]
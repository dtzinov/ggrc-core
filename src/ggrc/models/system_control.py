
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class SystemControl(Base, db.Model):
  __tablename__ = 'system_controls'

  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  state = db.Column(db.Integer, default=1, nullable=False)
  cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))
  cycle = db.relationship('Cycle', uselist=False)

  _publish_attrs = [
      'system',
      'control',
      'state',
      'cycle',
      ]
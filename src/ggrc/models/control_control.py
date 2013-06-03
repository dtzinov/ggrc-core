
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class ControlControl(Base, db.Model):
  __tablename__ = 'control_controls'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  implemented_control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))

  _publish_attrs = [
    'control',
    'implemented_control',
    ]
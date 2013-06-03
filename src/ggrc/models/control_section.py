
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class ControlSection(Base, db.Model):
  __tablename__ = 'control_sections'

  control_id = db.Column(db.Integer, db.ForeignKey('controls.id'))
  section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

  _publish_attrs = [
      'control',
      'section',
      ]

# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class SystemSystem(Base, db.Model):
  __tablename__ = 'system_systems'

  parent_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  child_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  type = db.Column(db.String)
  order = db.Column(db.Integer)

  _publish_attrs = [
      'parent',
      'child',
      'type',
      'order',
      ]

# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Identifiable, created_at_args

class ActivityLog(Identifiable, db.Model):
  __tablename__ = 'activity_logs'

  person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  created_at = db.Column(db.DateTime, **created_at_args())
  http_method = db.Column(db.String)
  resource_id = db.Column(db.Integer)
  resource_type = db.Column(db.String)
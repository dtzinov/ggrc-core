
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Identifiable, Described
from datetime import datetime
class LogEvent(Identifiable, Described, db.Model):
  __tablename__ = 'log_events'

  severity = db.Column(db.String)
  whodunnit = db.Column(db.String)
  created_at = db.Column(db.DateTime)
  updated_at = datetime.utcnow()

  _publish_attrs = [
      'severity',
      'whodunnit',
      'created_at',
      ]
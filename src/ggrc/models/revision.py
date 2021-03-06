
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Identifiable, created_at_args

class Revision(Identifiable, db.Model):
  __tablename__ = 'revisions'

  created_at = db.Column(db.DateTime, **created_at_args())
  person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  resource_id = db.Column(db.Integer)
  resource_type = db.Column(db.String)
  activity_id = db.Column(db.Integer, db.ForeignKey('activity_logs.id'))
  action = db.Column(db.String)
  content = db.Column(db.String)
  summary = db.Column(db.String)
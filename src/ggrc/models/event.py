
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Identifiable, created_at_args

class Event(Identifiable, db.Model):
  __tablename__ = 'events'

  person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = False)
  created_at = db.Column(db.DateTime, nullable = False, **created_at_args())
  http_method = db.Column(db.String, nullable = False)
  resource_id = db.Column(db.Integer, nullable = False)
  resource_type = db.Column(db.String, nullable = False)

  events = db.relationship('Revision', backref='event', lazy='subquery') # We always need the revisions
  person = db.relationship('Person')

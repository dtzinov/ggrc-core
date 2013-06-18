
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: vraj@reciprocitylabs.com
# Maintained By: vraj@reciprocitylabs.com

from ggrc import db
from .mixins import Identifiable, created_at_args

class Revision(Identifiable, db.Model):
  __tablename__ = 'revisions'

  resource_id = db.Column(db.Integer, nullable = False)
  resource_type = db.Column(db.String, nullable = False)
  event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable = False)
  action = db.Column(db.Enum(u'created', u'modified', u'deleted'), nullable = False)
  content = db.Column(db.String, nullable = False)

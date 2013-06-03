
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class Meeting(Base, db.Model):
  __tablename__ = 'meetings'

  response_id = db.Column(db.Integer, db.ForeignKey('responses.id'))
  start_at = db.Column(db.DateTime)
  calendar_url = db.Column(db.String)

  _publish_attrs = [
      'response',
      'start_at',
      'calendar_url',
      ]
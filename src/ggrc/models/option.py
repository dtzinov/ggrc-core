
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base, Described

class Option(Base, Described, db.Model):
  __tablename__ = 'options'

  role = db.Column(db.String)
  title = db.Column(db.String)
  required = db.Column(db.Boolean)

  _publish_attrs = [
      'role',
      'title',
      'required',
      ]
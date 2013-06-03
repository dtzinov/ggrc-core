
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base, Described

class Transaction(Base, Described, db.Model):
  __tablename__ = 'transactions'

  title = db.Column(db.String)
  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))

  _publish_attrs = [
      'title',
      'system',
      ]
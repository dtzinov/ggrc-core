
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Slugged

class Help(Slugged, db.Model):
  __tablename__ = 'helps'

  content = db.Column(db.Text)
  
  _publish_attrs = [
      'content',
      ]
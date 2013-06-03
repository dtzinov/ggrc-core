
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base

class ProgramDirective(Base, db.Model):
  __tablename__ = 'program_directives'

  program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))

  _publish_attrs = [
      'program',
      'directive',
      ]
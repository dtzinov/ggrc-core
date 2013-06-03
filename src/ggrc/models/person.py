
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import Base
from .reflection import PublishOnly

class Person(Base, db.Model):
  __tablename__ = 'people'

  email = db.Column(db.String)
  name = db.Column(db.String)
  language_id = db.Column(db.Integer)
  company = db.Column(db.String)
  object_people = db.relationship('ObjectPerson', backref='person')
  language = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Person.language_id) == Option.id, '\
                       'Option.role == "person_language")',
      uselist=False,
      )

  _publish_attrs = [
      'company',
      'email',
      'language',
      'name',
      PublishOnly('object_people'),
      ]
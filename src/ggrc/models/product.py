
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from .mixins import BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable

class Product(Documentable, Personable, Timeboxed, BusinessObject, db.Model):
  __tablename__ = 'products'

  type_id = db.Column(db.Integer)
  version = db.Column(db.String)
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Product.type_id) == Option.id, '\
                       'Option.role == "product_type")',
      uselist=False,
      )

  _publish_attrs = [
      'type',
      'version',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Product, cls).eager_query()
    return query.options(orm.joinedload('type'))
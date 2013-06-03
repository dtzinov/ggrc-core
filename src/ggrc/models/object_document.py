
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base, Timeboxed
from .reflection import PublishOnly

class ObjectDocument(Base, Timeboxed, db.Model):
  __tablename__ = 'object_documents'

  role = db.Column(db.String)
  notes = db.Column(db.Text)
  document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))

  # TODO: Polymorphic relationship
  documentable_id = db.Column(db.Integer)
  documentable_type = db.Column(db.String)

  @property
  def documentable_attr(self):
    return '{0}_documentable'.format(self.documentable_type)

  @property
  def documentable(self):
    return getattr(self, self.documentable_attr)

  @documentable.setter
  def documentable(self, value):
    return setattr(self, self.documentable_attr, value)

  _publish_attrs = [
      'role',
      'notes',
      'document',
      'documentable',
      ]

class Documentable(object):
  @declared_attr
  def object_documents(cls):
    cls.documents = association_proxy(
        'object_documents', 'document',
        creator=lambda document: ObjectDocument(
            document=document,
            modified_by_id=1,
            documentable_type=cls.__name__,
            )
        )
    joinstr = 'and_(foreign(ObjectDocument.documentable_id) == {type}.id, '\
                   'foreign(ObjectDocument.documentable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'ObjectDocument',
        primaryjoin=joinstr,
        backref='{0}_documentable'.format(cls.__name__),
        )

  _publish_attrs = [
      'documents',
      PublishOnly('object_documents'),
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Documentable, cls).eager_query()
    return query.options(orm.subqueryload_all('object_documents.document'))
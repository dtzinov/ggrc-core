from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declared_attr
from .mixins import Base, Timeboxed

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
    return '{}_documentable'.format(self.documentable_type)

  @property
  def documentable(self):
    return getattr(self, self.documentable_attr)

  @documentable.setter
  def documentable(self, value):
    return setattr(self, self.documentable_attr, value)

class Documentable(object):
  @declared_attr
  def object_documents(cls):
    cls.documents = association_proxy(
        'object_documents', 'document',
        creator=lambda document: ObjectDocument(
            document=document,
            modified_by_id=1,
            personable_type=cls.__name__,
            )
        )
    joinstr = 'and_(foreign(ObjectDocument.documentable_id) == {type}.id, '\
                   'foreign(ObjectDocument.documentable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'ObjectDocument',
        primaryjoin=joinstr,
        backref='{}_documentable'.format(cls.__name__),
        )

  _publish_attrs = [
      'documents',
      'object_documents',
      ]
  _update_attrs = []

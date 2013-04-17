from ggrc import db
from .mixins import Base, Timeboxed

class ObjectDocument(Base, Timeboxed, db.Model):
  __tablename__ = 'object_documents'

  role = db.Column(db.String)
  notes = db.Column(db.Text)
  document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))

  # TODO: Polymorphic relationship
  documentable_id = db.Column(db.Integer)
  documentable_type = db.Column(db.String)

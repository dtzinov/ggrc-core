from ggrc import db
from .mixins import Base

class Document(Base, db.Model):
  __tablename__ = 'documents'

  title = db.Column(db.String)
  link = db.Column(db.String)
  description = db.Column(db.Text)
  type_id = db.Column(db.Integer)
  kind_id = db.Column(db.Integer)
  year_id = db.Column(db.Integer)
  language_id = db.Column(db.Integer)
  object_documents = db.relationship('ObjectDocument', backref='document')
  population_worksheets_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.population_document_id',
      backref='population_document',
      )
  sample_worksheets_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.sample_worksheet_document_id',
      backref='sample_worksheet_document',
      )
  sample_evidences_documented = db.relationship(
      'PopulationSample',
      foreign_keys='PopulationSample.sample_evidence_document_id',
      backref='sample_evidence_document',
      )
  type = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.type_id) == Option.id, '\
                       'Option.role == "document_type")',
      uselist=False,
      )
  kind = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.kind_id) == Option.id, '\
                       'Option.role == "reference_type")',
      uselist=False,
      )
  year = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.year_id) == Option.id, '\
                       'Option.role == "document_year")',
      uselist=False,
      )
  language = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Document.language_id) == Option.id, '\
                       'Option.role == "language")',
      uselist=False,
      )

  _publish_attrs = [
      'title',
      'link',
      'description',
      'object_documents',
      'population_worksheets_documented',
      'sample_worksheets_documented',
      'sample_evidences_documented',
      'type',
      'kind',
      'year',
      'language',
      ]

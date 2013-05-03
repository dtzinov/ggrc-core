from ggrc import db
from .mixins import Base

class PopulationSample(Base, db.Model):
  __tablename__ = 'population_samples'

  response_id = db.Column(db.Integer, db.ForeignKey('responses.id'))
  population_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
  population = db.Column(db.Integer)
  sample_worksheet_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
  samples = db.Column(db.Integer)
  sample_evidence_document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))

  _publish_attrs = [
      'response',
      'population_document',
      'population',
      'sample_worksheet_document',
      'sample_evidence_document',
      ]

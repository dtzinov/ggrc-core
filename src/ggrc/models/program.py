from ggrc import db
from sqlalchemy.ext.associationproxy import association_proxy
from .mixins import BusinessObject, Timeboxed

class Program(BusinessObject, Timeboxed, db.Model):
  __tablename__ = 'programs'

  kind = db.Column(db.String)
  program_directives = db.relationship('ProgramDirective', backref='program')
  directives = association_proxy('program_directives', 'directive')
  cycles = db.relationship('Cycle', backref='program')

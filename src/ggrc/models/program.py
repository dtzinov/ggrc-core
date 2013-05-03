from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, Timeboxed

class Program(BusinessObject, Timeboxed, db.Model):
  __tablename__ = 'programs'

  KINDS = [
      'Directive',
      'Company Controls',
      ]

  KINDS_HIDDEN = [
      'Company Controls Policy',
      ]

  kind = db.Column(db.String)
  program_directives = db.relationship('ProgramDirective', backref='program')
  directives = association_proxy(
      'program_directives', 'directive', 'Directive')
  cycles = db.relationship('Cycle', backref='program')

  _publish_attrs = ['kind', 'program_directives', 'directives', 'cycles',]
  _update_attrs = ['kind', 'directives']

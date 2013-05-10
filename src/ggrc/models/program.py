from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable

class Program(Documentable, Personable, BusinessObject, Timeboxed, db.Model):
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
      'program_directives', 'directive', 'ProgramDirective')
  cycles = db.relationship('Cycle', backref='program')

  _publish_attrs = [
      'kind',
      'program_directives',
      'directives',
      'cycles',
      ]

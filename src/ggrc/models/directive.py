from ggrc import db
from .associationproxy import association_proxy
from .mixins import BusinessObject, Timeboxed
from .object_document import Documentable
from .object_person import Personable
from .reflection import PublishOnly

class Directive(Documentable, Personable, Timeboxed, BusinessObject, db.Model):
  __tablename__ = 'directives'

  company = db.Column(db.Boolean, default=False, nullable=False)
  version = db.Column(db.String)
  organization = db.Column(db.String)
  scope = db.Column(db.Text)
  kind_id = db.Column(db.Integer)
  audit_start_date = db.Column(db.DateTime)
  audit_frequency_id = db.Column(db.Integer)
  audit_duration_id = db.Column(db.Integer)
  kind = db.Column(db.String)
  sections = db.relationship(
      'Section', backref='directive', order_by='Section.slug')
  controls = db.relationship(
      'Control', backref='directive', order_by='Control.slug')
  program_directives = db.relationship('ProgramDirective', backref='directive')
  programs = association_proxy(
      'program_directives', 'program', 'ProgramDirective')
  audit_frequency = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Directive.audit_frequency_id) == Option.id, '\
                       'Option.role == "audit_frequency")',
      uselist=False,
      )
  audit_duration = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Directive.audit_duration_id) == Option.id, '\
                       'Option.role == "audit_duration")',
      uselist=False,
      )

  _publish_attrs = [
      'audit_start_date',
      'audit_frequency',
      'audit_duration',
      'company',
      'controls',
      'kind',
      'organization',
      'programs',
      PublishOnly('program_directives'),
      'scope',
      'sections',
      'version',
      ]

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Directive, cls).eager_query()
    return query.options(
        orm.joinedload('audit_frequency'),
        orm.joinedload('audit_duration'),
        orm.subqueryload('controls'),
        orm.subqueryload_all('program_directives.program'),
        orm.subqueryload('sections'))

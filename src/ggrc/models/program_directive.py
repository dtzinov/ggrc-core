from ggrc import db
from .mixins import Base

class ProgramDirective(Base, db.Model):
  __tablename__ = 'program_directives'

  program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
  directive_id = db.Column(db.Integer, db.ForeignKey('directives.id'))

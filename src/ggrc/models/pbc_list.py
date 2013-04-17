from ggrc import db
from .mixins import Base

class PbcList(Base, db.Model):
  __tablename__ = 'pbc_lists'

  audit_cycle_id = db.Column(db.Integer, db.ForeignKey('cycles.id'))

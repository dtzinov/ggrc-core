from ggrc import db
from .mixins import BusinessObject

class System(BusinessObject, db.Model):
  __tablename__ = 'systems'

  infrastructure = db.Column(db.Boolean)
  # TODO: unused?
  owner_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  is_biz_process = db.Column(db.Boolean, default=False)
  # TODO: handle option
  type_id = db.Column(db.Integer)
  version = db.Column(db.String)
  notes = db.Column(db.Text)
  # TODO: handle option
  network_zone_id = db.Column(db.Integer)

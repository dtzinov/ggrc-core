from ggrc import db
from .mixins import Slugged, Hyperlinked

class Directive(Slugged, Hyperlinked, db.Model):
  __tablename__ = 'directives'

  company = db.Column(db.Boolean, default=False, nullable=False)
  version = db.Column(db.String)
  #FIXME Can this be Timeboxed for these two fields?
  start_date = db.Column(db.DateTime)
  stop_date = db.Column(db.DateTime)
  organization = db.Column(db.String)
  scope = db.Column(db.Text)
  kind_id = db.Column(db.Integer)
  audit_start_date = db.Column(db.DateTime)
  audit_frequency_id = db.Column(db.Integer)
  audit_duration_id = db.Column(db.Integer)
  kind = db.Column(db.String)

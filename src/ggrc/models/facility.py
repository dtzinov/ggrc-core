from ggrc import db
from .mixins import Slugged

class Facility(Slugged, db.Model):
  __tablename__ = 'facilities'

  url = db.Column(db.String)
  start_date = db.Column(db.DateTime)
  stop_date = db.Column(db.DateTime)


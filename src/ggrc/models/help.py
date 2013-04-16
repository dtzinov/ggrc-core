from ggrc import db
from .mixins import Slugged

class Help(Slugged, db.Model):
  __tablename__ = 'helps'

  content = db.Column(db.Text)

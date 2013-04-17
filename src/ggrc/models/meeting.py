from ggrc import db
from .mixins import Base

class Meeting(Base, db.Model):
  __tablename__ = 'meetings'

  response_id = db.Column(db.Integer, db.ForeignKey('responses.id'))
  start_at = db.Column(db.DateTime)
  calendar_url = db.Column(db.String)

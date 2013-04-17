from ggrc import db
from .mixins import Base

class Response(Base, db.Model):
  __tablename__ = 'responses'

  request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
  system_id = db.Column(db.Integer, db.ForeignKey('systems.id'))
  status = db.Column(db.String)

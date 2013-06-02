from ggrc import db
from .mixins import Identifiable, created_at_args

class ActivityLog(Identifiable, db.Model):
  __tablename__ = 'activity_logs'

  person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
  created_at = db.Column(db.DateTime, **created_at_args())
  http_method = db.Column(db.String)
  resource_id = db.Column(db.Integer)
  resource_type = db.Column(db.String)

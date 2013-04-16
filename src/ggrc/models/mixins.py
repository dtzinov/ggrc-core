from ggrc import db

'''Mixins to add common attributes and relationships. Note, all model classes
must also inherit from ``db.Model``. For example:

  ..

     class Market(BusinessObject, db.Model):
       __tablename__ = 'markets'

'''

class Identifiable(object):
  '''A model with an ``id`` property that is the primary key.
  '''
  id = db.Column(db.Integer, primary_key=True)


class ChangeTracked(object):
  '''A model with fields to tracked the last user to modify the model, the
  creation time of the model, and the last time the model was updated.
  '''
  modified_by_id = db.Column(db.Integer, nullable=False)
  created_at = db.Column(
      db.DateTime, server_default=db.text('current_timestamp'))
  updated_at = db.Column(
      db.DateTime, server_onupdate=db.text('current_timestamp'))

class Described(object):
  description = db.Column(db.Text)

class Hyperlinked(object):
  url = db.Column(db.String)

class Child(object):
  parent_id = db.Column(db.Integer)

class Timeboxed(object):
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

class Base(Identifiable, ChangeTracked):
  '''Several of the models use the same mixins. This class covers that common
  case.
  '''
  pass

class Slugged(Base):
  '''Several classes make use of the common mixins and additional are
  "slugged" and have additional fields related to their publishing in the
  system.
  '''
  slug = db.Column(db.String, nullable=False)
  title = db.Column(db.String, nullable=False)

class BusinessObject(Slugged, Described, Hyperlinked):
  pass

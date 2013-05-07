from ggrc import settings, db
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

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

  # REST properties
  _publish_attrs = ['id']
  _update_attrs = []

def created_at_args():
  '''Sqlite doesn't have a server, per se, so the server_* args are useless.'''
  if settings.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
    return {'default': db.text('current_timestamp'),}
  return {'server_default': db.text('current_timestamp'),}

def updated_at_args():
  '''Sqlite doesn't have a server, per se, so the server_* args are useless.'''
  if settings.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
    return {
        'default': db.text('current_timestamp'),
        'onupdate': db.text('current_timestamp'),
        }
  return {
      'server_default': db.text('current_timestamp'),
      'server_onupdate': db.text('current_timestamp'),
      }

class ChangeTracked(object):
  '''A model with fields to tracked the last user to modify the model, the
  creation time of the model, and the last time the model was updated.
  '''
  modified_by_id = db.Column(db.Integer, nullable=False)
  created_at = db.Column(
      db.DateTime,
      **created_at_args())
  updated_at = db.Column(
      db.DateTime,
      **updated_at_args())
  #TODO Add a transaction id, this will be handy for generating etags
  #and for tracking the changes made to several resources together.
  #transaction_id = db.Column(db.Integer)

  # REST properties
  _publish_attrs = [
      #'modified_by_id' link to person??
      'created_at',
      'updated_at',
      ]
  _update_attrs = []

class Described(object):
  description = db.Column(db.Text)
  
  # REST properties
  _publish_attrs = ['description']

class Hyperlinked(object):
  url = db.Column(db.String)

  # REST properties
  _publish_attrs = ['url']

class Hierarchical(object):
  @declared_attr
  def parent_id(cls):
    return db.Column(
        db.Integer, db.ForeignKey('{}.id'.format(cls.__tablename__)))

  @declared_attr
  def children(cls):
    return db.relationship(
        cls.__name__,
        backref=db.backref('parent', remote_side='{}.id'.format(cls.__name__)),
        )

  # REST properties
  _publish_attrs = [
      'children',
      'parent',
      ]

class Timeboxed(object):
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

  # REST properties
  _publish_attrs = ['start_date', 'end_date']

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

  # REST properties
  _publish_attrs = ['slug', 'title']
  _update_attrs = ['title']
  _create_attrs = _publish_attrs

class BusinessObject(Slugged, Described, Hyperlinked):
  pass

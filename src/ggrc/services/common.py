import datetime
import hashlib
import json
import time
from flask.views import View
from flask import url_for, request, current_app
from ggrc import db
from wsgiref.handlers import format_date_time

class DateTimeEncoder(json.JSONEncoder):
  '''Custom JSON Encoder to handle datetime objects

  from:
     `http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime`_
  also consider:
     `http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53`_
  '''
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat()
    else:
      return super(DateTimeEncoder, self).default(obj)


# View base class for Views handling
#   - /resources (GET, POST)
#   - /resources/<pk:pk_type> (GET, PUT, POST, DELETE)
class Resource(View):
  '''View base class for Views handling.  Will typically be registered with an
  application following a collection style for routes. Collection ``GET`` and
  ``POST`` will have a route like ``/resources`` while collection member
  resource routes will have routes likej ``/resources/<pk:pk_type>``.

  To register a Resource subclass FooCollection with a Flask application:

  ..
     
     FooCollection.add_to(app, '/foos')

  By default will only support the ``application/json`` content-type.
  '''
  #methods = ['GET', 'PUT', 'POST', 'DELETE']
  pk = 'id'
  pk_type = 'int'

  _model = None
  _model_name = 'object'
  _model_plural = 'objects'

  def dispatch_request(self, *args, **kwargs):
    method = request.method.lower()

    if method == 'get':
      if self.pk in kwargs and kwargs[self.pk] is not None:
        return self.get(*args, **kwargs)
      else:
        return self.collection_get()
    elif method == 'post':
      if self.pk in kwargs and kwargs[self.pk] is not None:
        return self.post(*args, **kwargs)
      else:
        return self.collection_post()
      #return self.post(*args, **kwargs)
    elif method == 'put':
      return self.put(*args, **kwargs)
    elif method == 'delete':
      return self.delete(*args, **kwargs)
    else:
      raise NotImplementedError()

  def post(*args, **kwargs):
    raise NotImplementedError()

  # Default JSON request handlers
  def get(self, id):
    obj = self.get_object(id)

    if obj is None:
      return self.not_found_response()
    else:
      return self.json_success_response(
        self.object_for_json(obj), obj.updated_at)

  def put(self, id):
    obj = self.get_object(id)

    if obj is None:
      return self.not_found_response()
    else:
      self.update_object_from_form(obj, self.request.form)
      db.session.add(obj)
      db.session.commit()

      return self.json_success_response(
        self.object_as_json(obj), obj.updated_at)

  def delete(self, id):
    obj = self.get_object(id)

    if obj is None:
      return self.not_found_response()
    else:
      db.session.delete(obj)
      return self.json_success_response(
        self.object_as_json(obj), obj.updated_at)

  def collection_get(self):
    objs = self.get_collection()

    return self.json_success_response(
      self.collection_for_json(objs), self.collection_last_modified())

  def collection_post(self):
    obj = self.model()

    self.update_object_from_form(obj, self.request.form)

    db.session.add(obj)
    db.session.commit()

    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at)

  # Simple accessor properties
  @property
  def request(self):
    return request

  @property
  def model(self):
    return self._model

  # Model/DB Inspection
  # TODO: Fix -- this is cheating
  @property
  def model_name(self):
    if self.model is None:
      return self._model_name
    else:
      return self.model.__name__.lower()

  @property
  def model_plural(self):
    if self.model is None:
      return self._model_plural
    else:
      return self.model.__tablename__

  # Default model/DB helpers
  def get_collection(self):
    return db.session.query(self.model)

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection().filter(self.model.id == id).first()

  def update_object_from_form(self, category, form):
    return

  # Routing helpers
  @classmethod
  def endpoint_name(cls):
    return cls.__name__

  @classmethod
  def url_for(cls, *args, **kwargs):
    return url_for(cls.endpoint_name(), *args, **kwargs)

  @classmethod
  def add_to(cls, app, url):
    view_func = cls.as_view(cls.endpoint_name())
    app.add_url_rule(
        url,
        defaults={cls.pk: None},
        view_func=view_func,
        methods=['GET','POST'])
    app.add_url_rule(
        '%s/<%s:%s>' % (url, cls.pk_type, cls.pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])

  # Response helpers
  @classmethod
  def as_json(cls, obj, **kwargs):
    return json.dumps(obj, cls=DateTimeEncoder, **kwargs)

  def attrs_for_json(self, object):
    return {}

  def object_for_json(self, object, **kwargs):
    model_name = kwargs.get('model_name', self.model_name)

    object_for_json = {
      'id': object.id,
      'selfLink': self.url_for(id=object.id),
      'created_at': object.created_at,
      'updated_at': object.updated_at,
      }
    attrs_for_json = self.attrs_for_json(object)
    object_for_json.update(attrs_for_json)

    return { model_name: object_for_json }

  def collection_for_json(self, objects, **kwargs):
    model_name = kwargs.get('model_name', self.model_name)
    model_plural = kwargs.get('model_plural', self.model_plural)
    collection_name = kwargs.get('collection_name', '%s_collection' % (model_plural,))

    objects_json = []
    for object in objects:
      object_for_json = self.object_for_json(object, model_name=model_name)
      objects_json.append(object_for_json)

    collection_json = {
      collection_name: {
        'selfLink': self.url_for(),
        model_plural: objects_json,
        }
      }

    return collection_json

  def json_success_response(self, response_object, last_modified):
    last_modified = format_date_time(time.mktime(last_modified.utctimetuple()))
    headers = [
        ('Last-Modified', last_modified),
        ('Etag', self.etag(last_modified)),
        ('Content-Type', 'application/json'),
        ]
    return current_app.make_response(
      (self.as_json(response_object), 200, headers))

  def not_found_message(self):
    return '%s not found.' % (self.model_name.title(),)

  def not_found_response(self):
    return current_app.make_response((self.not_found_message(), 404, []))

  def etag(self, last_modified):
    '''Generate the etag given a datetime for the last time the resource was
    modified. This isn't as good as an etag generated off of a hash of the
    representation, but, it doesn't require the representation in order to be
    calculated. An alternative would be to keep an etag on the stored
    representation, but this will do for now.
    '''
    return '"{}"'.format(hashlib.sha1(last_modified).hexdigest())

  def collection_last_modified(self):
    '''Calculate the last time a member of the collection was modified. This
    method relies on the fact that the collection table has an ``updated_at``
    column; services for models that don't have this field **MUST** override
    this method.
    '''
    result = db.session.query(
        self.model.updated_at).order_by(self.model.updated_at).first()
    if result is not None:
      return result.updated_at 
    return datetime.datetime.now()

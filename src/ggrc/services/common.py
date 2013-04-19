import datetime
import hashlib
import json
import time
from flask import url_for, request, current_app
from flask.views import View
from ggrc import db
from types import MethodType
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
  application following a collection style for routes. Collection `GET` and
  `POST` will have a route like `/resources` while collection member
  resource routes will have routes likej `/resources/<pk:pk_type>`.

  To register a Resource subclass FooCollection with a Flask application:

  ..
     
     FooCollection.add_to(app, '/foos')

  By default will only support the `application/json` content-type.
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
    if 'Accept' in self.request.headers and \
       'application/json' not in self.request.headers['Accept']:
      return current_app.make_response((
        'application/json', 406, [('Content-Type', 'text/plain')]))
    object_for_json = self.object_for_json(obj)
    if 'If-None-Match' in self.request.headers and \
        self.request.headers['If-None-Match'] == self.etag(object_for_json):
      return current_app.make_response((
        '', 304, [('Etag', self.etag(object_for_json))]))
    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at)

  def validate_headers_for_put_or_delete(self, obj):
    missing_headers = []
    if 'If-Match' not in self.request.headers:
      missing_headers.append('If-Match')
    if 'If-Unmodified-Since' not in self.request.headers:
      missing_headers.append('If-Unmodified-Since')
    if missing_headers:
      # rfc 6585 defines a new status code for missing required headers
      return current_app.make_response((
        'If-Match is required.', 428, [('Content-Type', 'text/plain')]))
    if request.headers['If-Match'] != self.etag(self.object_for_json(obj)) or \
       request.headers['If-Unmodified-Since'] != \
          self.http_timestamp(obj.updated_at):
      return current_app.make_response((
          'The resource has been changed. The conflict must be resolved and '
          'the request resubmitted with an up to date Etag for If-Match '
          'header.',
          409,
          [('Content-Type', 'text/plain')]
          ))
    return None

  def put(self, id):
    obj = self.get_object(id)
    if obj is None:
      return self.not_found_response()
    if self.request.headers['Content-Type'] != 'application/json':
      return current_app.make_response((
        'Content-Type must be application/json', 415,[]))
    header_error = self.validate_headers_for_put_or_delete(obj)
    if header_error:
      return header_error
    self._update_object(obj, self.request.json)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = 1
    db.session.add(obj)
    db.session.commit()
    obj = self.get_object(id)
    return self.json_success_response(
        self.object_for_json(obj), obj.updated_at)

  def delete(self, id):
    obj = self.get_object(id)

    if obj is None:
      return self.not_found_response()
    header_error = self.validate_headers_for_put_or_delete(obj)
    if header_error:
      return header_error
    db.session.delete(obj)
    db.session.commit()
    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at)

  def collection_get(self):
    if 'Accept' in self.request.headers and \
       'application/json' not in self.request.headers['Accept']:
      return current_app.make_response((
        'application/json', 406, [('Content-Type', 'text/plain')]))

    objs = self.get_collection()

    return self.json_success_response(
      self.collection_for_json(objs), self.collection_last_modified())

  def collection_post(self):
    if self.request.headers['Content-Type'] != 'application/json':
      return current_app.make_response((
        'Content-Type must be application/json', 415,[]))
    obj = self.model()
    src = self.request.json
    self._update_object(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = 1
    db.session.add(obj)
    db.session.commit()
    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at, id=obj.id, status=201)

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
    return db.session.query(self.model).order_by(self.model.updated_at.desc())

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection().filter(self.model.id == id).first()

  def _update_object_for(self, base, obj, src):
    method = getattr(base, 'update_object', None)
    if method and isinstance(method, MethodType):
      method(self, obj, src)

  def _update_object(self, obj, src):
    for base in self.__class__.__bases__:
      self._update_object_for(base, obj, src)
    self._update_object_for(self.__class__, obj, src)

  def update_object(self, obj, src):
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

  def _attrs_for_json_from(self, base, obj):
    '''Return all attributes to contribute to the JSON representation of this
    object that are contributed from the base class `base` for the given
    model object `obj`.
    '''
    method = getattr(base, 'attrs_for_json', None)
    if method and isinstance(method, MethodType):
      return method(self, obj)

  def _attrs_for_json(self, obj):
    '''Build up the json representation of the object by walking all base
    clases and gathering their contributions and finally adding the
    contributions from the instance's concrete class.
    '''
    attrs = {}
    for base in self.__class__.__bases__:
      attrs.update(self._attrs_for_json_from(base, obj))
    attrs.update(self._attrs_for_json_from(self.__class__, obj))
    return attrs

  def attrs_for_json(self, obj):
    '''All mixin classes and subclasses that have content to contribute to the
    JSON representation of the model instance `obj` **MUST** implement this
    method.

    Refer to `_attrs_for_json` to see how this is performed.
    '''
    return {}

  def object_for_json(self, object, model_name=None):
    model_name = model_name or self.model_name
    return { model_name: self.object_for_json_container(object) }

  def object_for_json_container(self, object):
    object_for_json = {
      'id': object.id,
      'selfLink': self.url_for(id=object.id),
      'created_at': object.created_at,
      'updated_at': object.updated_at,
      }
    attrs_for_json = self._attrs_for_json(object)
    object_for_json.update(attrs_for_json)
    return object_for_json

  def collection_for_json(
      self, objects, model_plural=None, collection_name=None):
    model_plural = model_plural or self.model_plural
    collection_name = collection_name or '%s_collection' % (model_plural,)

    objects_json = []
    for object in objects:
      object_for_json = self.object_for_json_container(object)
      objects_json.append(object_for_json)

    collection_json = {
      collection_name: {
        'selfLink': self.url_for(),
        model_plural: objects_json,
        }
      }

    return collection_json

  def http_timestamp(self, timestamp):
    return format_date_time(time.mktime(timestamp.utctimetuple()))

  def json_success_response(
      self, response_object, last_modified, status=200, id=None):
    headers = [
        ('Last-Modified', self.http_timestamp(last_modified)),
        ('Etag', self.etag(response_object)),
        ('Content-Type', 'application/json'),
        ]
    if id:
      headers.append(('Location', self.url_for(id=id)))
    return current_app.make_response(
      (self.as_json(response_object), status, headers))

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

    .. note::
      
       Using the datetime implies the need for some care - the resolution of
       the time object needs to be sufficient such that you don't end up with
       the same etag due to two updates performed in rapid succession.
    '''
    return '"{}"'.format(hashlib.sha1(str(last_modified)).hexdigest())

  def collection_last_modified(self):
    '''Calculate the last time a member of the collection was modified. This
    method relies on the fact that the collection table has an `updated_at`
    column; services for models that don't have this field **MUST** override
    this method.
    '''
    result = db.session.query(
        self.model.updated_at).order_by(self.model.updated_at.desc()).first()
    if result is not None:
      return result.updated_at 
    return datetime.datetime.now()

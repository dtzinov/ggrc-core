import datetime
import ggrc.builder.json
import hashlib
import iso8601
import json
import time
from flask import url_for, request, current_app
from flask.views import View
from ggrc import db
from ggrc.fulltext import get_indexer
from ggrc.fulltext.recordbuilder import fts_record_for
from sqlalchemy import and_, cast
from sqlalchemy.types import AbstractType, Boolean, Date, DateTime
from werkzeug.exceptions import BadRequest
from wsgiref.handlers import format_date_time

"""gGRC Collection REST services implementation. Common to all gGRC collection
resources.
"""

class DateTimeEncoder(json.JSONEncoder):
  """Custom JSON Encoder to handle datetime objects

  from:
     `http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime`_
  also consider:
     `http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53`_
  """
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat()
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat()
    else:
      return super(DateTimeEncoder, self).default(obj)

class UnicodeSafeJsonWrapper(dict):
  """JSON received via POST has keys as unicode. This makes get work with plain
  `str` keys.
  """
  def __getitem__(self, key):
    ret = self.get(key)
    if ret is None:
      raise KeyError(key)
    return ret

  def get(self, key, default=None):
    return super(UnicodeSafeJsonWrapper, self).get(unicode(key), default)

class BadQueryParameter(BadRequest):
  """Temporary distinction to allow unkown query parameters through without
  breaking request format checking for other things like Date, Datetime, and
  Boolean
  """
  def __init__(self, message):
    super(BadQueryParameter, self).__init__(message)

class ModelView(View):
  pk = 'id'
  pk_type = 'int'

  _model = None
  _model_name = 'object'
  _model_plural = 'objects'

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
    if hasattr(self.model, 'eager_query'):
      query = self.model.eager_query()
    else:
      query = db.session.query(self.model)
    if request.args:
      try:
        query = query.filter(self.collection_filters())
      #FIXME neither of the except handlers should be needed.
      #except BadQueryParameter:
      except BadRequest:
        pass
    return query.order_by(self.model.updated_at.desc())

  def get_attr_for_query_param(self, attrname):
    #FIXME Differentiating bad parameter to allow it through, for now
    #badrequest = lambda: BadRequest(
    badrequest = lambda: BadQueryParameter(
        'Unknown or unsupported query parameter {0}'.format(attrname))
    if not hasattr(self.model, attrname):
      raise badrequest()
    attr = getattr(self.model, attrname)
    if not hasattr(attr, 'type') or \
        not isinstance(attr.type, AbstractType):
      raise badrequest()
    return attr

  def coerce_value_for_query_param(self, attr, arg, value):
    attr_type = type(attr.type)
    if attr_type is Boolean:
      value = value.lower()
      if value == 'true':
        value = True
      elif value == 'false':
        value = False
      else:
        raise BadRequest('{0} must be "true" or "false", not {1}.'.format(
          arg, value))
    elif attr_type is DateTime:
      try:
       value = iso8601.parse_date(value)
      except iso8601.ParseError as e:
        raise BadRequest(
            'Malformed DateTime {0} for parameter {0}. '
            'Error message was: {1}'.format(value, arg, e.message)
            )
    elif attr_type is Date:
      try:
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
      except ValueError as e:
        raise BadRequest(
            'Malformed Date {0} for parameter {1}. '
            'Error message was: {2}'.format(value, arg, e.message)
            )
    return value

  def collection_filters(self):
    """Create filter expressions using ``request.args``"""
    filter_expressions = None
    for arg, value in request.args.items():
      attr = self.get_attr_for_query_param(arg)
      value = self.coerce_value_for_query_param(attr, arg, value)
      if filter_expressions:
        filter_expressions = and_(
            filter_expressions, attr == cast(value, attr.type))
      else:
        filter_expressions = attr == cast(value, attr.type)
    return filter_expressions

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection().filter(self.model.id == id).first()

  def not_found_message(self):
    return '%s not found.' % (self.model_name.title(),)

  def not_found_response(self):
    return current_app.make_response((self.not_found_message(), 404, []))

  def etag(self, last_modified):
    """Generate the etag given a datetime for the last time the resource was
    modified. This isn't as good as an etag generated off of a hash of the
    representation, but, it doesn't require the representation in order to be
    calculated. An alternative would be to keep an etag on the stored
    representation, but this will do for now.

    .. note::

       Using the datetime implies the need for some care - the resolution of
       the time object needs to be sufficient such that you don't end up with
       the same etag due to two updates performed in rapid succession.
    """
    return '"{0}"'.format(hashlib.sha1(str(last_modified)).hexdigest())

  def collection_last_modified(self):
    """Calculate the last time a member of the collection was modified. This
    method relies on the fact that the collection table has an `updated_at`
    column; services for models that don't have this field **MUST** override
    this method.
    """
    result = db.session.query(
        self.model.updated_at).order_by(self.model.updated_at.desc()).first()
    if result is not None:
      return result.updated_at
    return datetime.datetime.now()

  # Routing helpers
  @classmethod
  def endpoint_name(cls):
    return cls.__name__

  @classmethod
  def url_for(cls, *args, **kwargs):
    if args and isinstance(args[0], db.Model):
      return url_for(cls.endpoint_name(), *args[1:], id=args[0].id, **kwargs)
    return url_for(cls.endpoint_name(), *args, **kwargs)


# View base class for Views handling
#   - /resources (GET, POST)
#   - /resources/<pk:pk_type> (GET, PUT, POST, DELETE)
class Resource(ModelView):
  """View base class for Views handling.  Will typically be registered with an
  application following a collection style for routes. Collection `GET` and
  `POST` will have a route like `/resources` while collection member
  resource routes will have routes likej `/resources/<pk:pk_type>`.

  To register a Resource subclass FooCollection with a Flask application:

  ..

     FooCollection.add_to(app, '/foos')

  By default will only support the `application/json` content-type.
  """

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
    src = UnicodeSafeJsonWrapper(self.request.json)
    try:
      src = src[self.model_name]
    except KeyError, e:
      return current_app.make_response((
        'Required attribute "%s" not found' % self.model_name, 400, []))
    ggrc.builder.json.update(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = 1
    db.session.add(obj)
    db.session.commit()
    obj = self.get_object(id)
    get_indexer().update_record(fts_record_for(obj))
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
    get_indexer().delete_record(self.url_for(id=id))
    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at)

  def collection_get(self):
    if 'Accept' in self.request.headers and \
       'application/json' not in self.request.headers['Accept']:
      return current_app.make_response((
        'application/json', 406, [('Content-Type', 'text/plain')]))

    objs = self.get_collection()
    collection = self.collection_for_json(objs)
    if 'If-None-Match' in self.request.headers and \
        self.request.headers['If-None-Match'] == self.etag(collection):
      return current_app.make_response((
        '', 304, [('Etag', self.etag(collection))]))
    return self.json_success_response(
      collection, self.collection_last_modified())

  def collection_post(self):
    if self.request.headers['Content-Type'] != 'application/json':
      return current_app.make_response((
        'Content-Type must be application/json', 415,[]))
    obj = self.model()
    src = UnicodeSafeJsonWrapper(self.request.json)
    try:
      src = src[self.model_name]
    except KeyError, e:
      return current_app.make_response((
        'Required attribute "%s" not found' % self.model_name, 400, []))
    ggrc.builder.json.create(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = 1
    db.session.add(obj)
    db.session.commit()
    get_indexer().create_record(fts_record_for(obj))
    return self.json_success_response(
      self.object_for_json(obj), obj.updated_at, id=obj.id, status=201)

  @classmethod
  def add_to(cls, app, url, model_class=None):
    if model_class:
      service_class = type(model_class.__name__, (Resource,), {
        '_model': model_class,
        })
      import ggrc.services
      setattr(ggrc.services, model_class.__name__, service_class)
    else:
      service_class = cls
    view_func = service_class.as_view(service_class.endpoint_name())
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

  def object_for_json(self, obj, model_name=None):
    model_name = model_name or self.model_name
    json_obj = ggrc.builder.json.publish(obj)
    return { model_name: json_obj }

  def collection_for_json(
      self, objects, model_plural=None, collection_name=None):
    model_plural = model_plural or self.model_plural
    collection_name = collection_name or '%s_collection' % (model_plural,)

    objects_json = []
    for object in objects:
      object_for_json = ggrc.builder.json.publish(object)
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

  def getval(self, src, attr, *args):
    if args:
      return src.get(unicode(attr), *args)
    return src.get(unicode(attr))

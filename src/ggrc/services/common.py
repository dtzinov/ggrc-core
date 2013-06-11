# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import datetime
import ggrc.builder.json
import hashlib
import json
import time
from flask import url_for, request, current_app
from flask.views import View
from ggrc import db
from ggrc.fulltext import get_indexer
from ggrc.fulltext.recordbuilder import fts_record_for
from ggrc.login import get_current_user_id
from werkzeug.exceptions import BadRequest
from wsgiref.handlers import format_date_time
from .attribute_query import AttributeQueryBuilder

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

def as_json(obj, **kwargs):
  return json.dumps(obj, cls=DateTimeEncoder, **kwargs)

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

  @property
  def modified_attr_name(self):
    return 'updated_at'

  @property
  def modified_attr(self):
    """Return the model attribute to be used for Last-Modified header and
    sorting collection elements.
    """
    return getattr(self.model, self.modified_attr_name)

  def modified_at(self, obj):
    return getattr(obj, self.modified_attr_name)

  # Default model/DB helpers
  def get_collection(self):
    if hasattr(self.model, 'eager_query'):
      query = self.model.eager_query()
    else:
      query = db.session.query(self.model)
    if request.args:
      querybuilder = AttributeQueryBuilder(self.model)
      filter, joinlist = querybuilder.collection_filters(request.args)
      if filter is not None:
        for j in joinlist:
          query = query.join(j)
        query = query.filter(filter)
    return query.order_by(self.modified_attr.desc())

  def get_object(self, id):
    # This could also use `self.pk`
    return self.get_collection().filter(self.model.id == id).first()

  def not_found_message(self):
    return '{0} not found.'.format(self.model_name.title())

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
    method relies on the fact that the collection table has an `updated_at` or
    other column with a relevant timestamp; services for models that don't have
    this field **MUST** override this method.
    """
    result = db.session.query(
        self.modified_attr).order_by(self.modified_attr.desc()).first()
    if result is not None:
      return self.modified_at(result)
    return datetime.datetime.now()

  # Routing helpers
  @classmethod
  def endpoint_name(cls):
    return cls.__name__

  @classmethod
  def url_for(cls, *args, **kwargs):
    if args and isinstance(args[0], db.Model):
      return url_for(cls.endpoint_name(), *args[1:], id=args[0].id, **kwargs)
    # preserve original query string
    idx = request.url.find('?')
    querystring = '' if idx < 0 else '?' + request.url[idx+1:]
    return url_for(cls.endpoint_name(), *args, **kwargs) + querystring

  @classmethod
  def decorate_view_func(cls, view_func, decorators):
    if not isinstance(decorators, (list, tuple)):
      decorators = (decorators,)
    for decorator in reversed(decorators):
      view_func = decorator(view_func)
    return view_func


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
      self.object_for_json(obj), self.modified_at(obj))

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
          self.http_timestamp(self.modified_at(obj)):
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
        'Required attribute "{0}" not found'.format(self.model_name), 400, []))
    ggrc.builder.json.update(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = get_current_user_id()
    db.session.add(obj)
    db.session.commit()
    obj = self.get_object(id)
    get_indexer().update_record(fts_record_for(obj))
    return self.json_success_response(
        self.object_for_json(obj), self.modified_at(obj))

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
      self.object_for_json(obj), self.modified_at(obj))

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
        'Required attribute "{0}" not found'.format(self.model_name), 400, []))
    ggrc.builder.json.create(obj, src)
    #FIXME Fake the modified_by_id until we have that information in session.
    obj.modified_by_id = get_current_user_id()
    db.session.add(obj)
    db.session.commit()
    get_indexer().create_record(fts_record_for(obj))
    return self.json_success_response(
      self.object_for_json(obj), self.modified_at(obj), id=obj.id, status=201)

  @classmethod
  def add_to(cls, app, url, model_class=None, decorators=()):
    if model_class:
      service_class = type(model_class.__name__, (Resource,), {
        '_model': model_class,
        })
      import ggrc.services
      setattr(ggrc.services, model_class.__name__, service_class)
    else:
      service_class = cls
    view_func = service_class.as_view(service_class.endpoint_name())
    view_func = cls.decorate_view_func(view_func, decorators)
    app.add_url_rule(
        url,
        defaults={cls.pk: None},
        view_func=view_func,
        methods=['GET','POST'])
    app.add_url_rule(
        '{url}/<{type}:{pk}>'.format(url=url, type=cls.pk_type, pk=cls.pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE'])

  # Response helpers
  @classmethod
  def as_json(cls, obj, **kwargs):
    return as_json(obj, **kwargs)

  def object_for_json(self, obj, model_name=None):
    model_name = model_name or self.model_name
    json_obj = ggrc.builder.json.publish(obj)
    return { model_name: json_obj }

  def get_properties_to_include(self):
    #FIXME This needs to be improved to deal with branching paths... if that's
    #desirable or needed.
    inclusions = request.args.get('__include')
    if inclusions is not None:
      if len(inclusions) == 0:
        raise BadRequest(
            'The __include query parameter requires at least one field to be '
            'included.')
      paths = inclusions.split(',')
      inclusions = []
      for p in paths:
        path = p.split('.')
        if len(path) == 1:
          inclusions.append(path)
        else:
          inclusions.append((path[0], path[1:]))
    else:
      inclusions = ()
    return inclusions

  def collection_for_json(
      self, objects, model_plural=None, collection_name=None):
    model_plural = model_plural or self.model_plural
    collection_name = collection_name or '{0}_collection'.format(model_plural)

    objects_json = []
    for object in objects:
      object_for_json = ggrc.builder.json.publish(
          object, self.get_properties_to_include())
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

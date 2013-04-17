from flask.views import View
from flask import url_for, request, current_app
from ggrc import db


# Custom JSONEncoder to handle datetime objects
import json
import datetime

# from:
#   http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime
# also consider:
#   http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53
class DateTimeEncoder(json.JSONEncoder):
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

  # Default request handlers
  #def get(*args, **kwargs):
  #  raise NotImplementedError()

  #def put(*args, **kwargs):
  #  raise NotImplementedError()

  #def delete(*args, **kwargs):
  #  raise NotImplementedError()

  def post(*args, **kwargs):
    raise NotImplementedError()

  #def collection_get(*args, **kwargs):
  #  raise NotImplementedError()

  #def collection_post(*args, **kwargs):
  #  raise NotImplementedError()

  # Default JSON request handlers
  def get(self, id):
    category = self.get_object(id)

    if category is None:
      return self.not_found_response()
    else:
      return self.json_success_response(
        self.object_for_json(category))

  def put(self, id):
    category = self.get_object(id)

    if category is None:
      return self.not_found_response()
    else:
      self.update_object_from_form(category, self.request.form)
      db.session.add(category)
      db.session.commit()

      return self.json_success_response(
        self.object_as_json(category))

  def delete(self, id):
    category = self.get_object(id)

    if category is None:
      return self.not_found_response()
    else:
      db.session.delete(category)
      return self.json_success_response(
        self.object_as_json(category))

  def collection_get(self):
    categories = self.get_collection()

    return self.json_success_response(
      self.collection_for_json(categories))

  def collection_post(self):
    category = self.model()

    self.update_object_from_form(category, self.request.form)

    db.session.add(category)
    db.session.commit()

    return self.json_success_response(
      self.object_for_json(category))

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

  def json_success_response(self, response_object):
    return current_app.make_response(
      (self.as_json(response_object), 200, []))

  def not_found_message(self):
    return '%s not found.' % (self.model_name.title(),)

  def not_found_response(self):
    return current_app.make_response((self.not_found_message(), 404, []))


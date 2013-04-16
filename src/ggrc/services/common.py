from flask.views import View
from flask import url_for, request


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
  def get(*args, **kwargs):
    raise NotImplementedError()

  def put(*args, **kwargs):
    raise NotImplementedError()

  def delete(*args, **kwargs):
    raise NotImplementedError()

  def post(*args, **kwargs):
    raise NotImplementedError()

  def collection_get(*args, **kwargs):
    raise NotImplementedError()

  def collection_post(*args, **kwargs):
    raise NotImplementedError()

  # Simple accessor properties
  @property
  def request(self):
    return request

  @property
  def model(self):
    return self._model

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


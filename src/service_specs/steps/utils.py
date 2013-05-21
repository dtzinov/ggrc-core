"""Provide commonly-used methods here.

Don't use ``@when``, ``@given``, etc. here, as it will raise
``behave.step_registry.AmbiguousStep``, since this module is included in
multiple steps/*.py modules.
"""

import json
import datetime
from factories import factory_for

class Example(object):
  """An example resource for use in a behave scenario, by name."""
  def __init__(self, resource_type, value):
    self.resource_type = resource_type
    self.value = value

  def get(self, attr):
    return self.value.get(get_resource_table_singular(self.resource_type)).get(attr)

  def set(self, attr, value):
    self.value[attr] = value

def set_property(obj, attr, value):
  if isinstance(obj, Example):
    obj.set(attr, value)
  else:
    setattr(obj, attr, value)


def handle_example_resource(context, resource_type):
  resource_factory = factory_for(resource_type)
  context.example_resource = resource_factory()

def handle_named_example_resource(context, resource_type, name, **kwargs):
  resource_factory = factory_for(resource_type)
  example = Example(resource_type, resource_factory(**kwargs))
  setattr(context, name, example)

def handle_get_resource_and_name_it(context, url, name):
  response = get_resource(context, url)
  assert response.status_code == 200
  setattr(context, name, response.json())

def get_resource(context, url):
  import requests
  return requests.get(
      context.base_url+url,
      headers={
        'Accept': 'application/json',
        },
      )

def handle_get_example_resource(context, name):
  example = getattr(context, name)
  url = example.get('selfLink')
  response = get_resource(context, url)
  assert response.status_code == 200
  example = Example(example.resource_type, response.json())
  setattr(context, name, example)  

def handle_post_named_example_to_collection_endpoint(context, name):
  example = getattr(context, name)
  url = get_service_endpoint_url(context, example.resource_type)
  handle_post_named_example(context, name, url)

def handle_post_named_example(context, name, url):
  example = getattr(context, name)
  response = post_example(
      context, example.resource_type, example.value, url)
  assert response.status_code == 201, \
      'Expected status code 201, received {0}'.format(response.status_code)
  example = Example(example.resource_type, response.json())
  setattr(context, name, example)

def post_example(context, resource_type, example, url):
  #For **some** reason, I can't import this at the module level in a steps file
  import requests
  data = json.dumps(
      {get_resource_table_singular(resource_type): example},
      cls=DateTimeEncoder,
      )
  return requests.post(
      context.base_url+url,
      data=data,
      headers={
        'Content-Type': 'application/json',
        },
      )

class DateTimeEncoder(json.JSONEncoder):
  """Custom JSON Encoder to handle datetime objects

  from:
     `http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime`_
  also consider:
     `http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53`_
  """
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat('T')
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat('T')
    else:
      return super(DateTimeEncoder, self).default(obj)

def get_resource_table_singular(resource_type):
  # This should match the implementation at
  #   ggrc.models.inflector:ModelInflector.underscore_from_camelcase
  import re
  s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', resource_type)
  return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def get_service_endpoint_url(context, endpoint_name):
  """Return the URL for the `endpoint_name`. This assumes that there is a
  `service_description` in the `context` to ues to lookup the endpoint url.
  """
  return context.service_description.get(u'service_description')\
      .get(u'endpoints').get(unicode(endpoint_name)).get(u'href')

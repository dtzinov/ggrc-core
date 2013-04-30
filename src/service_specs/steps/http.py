import datetime
import json
from behave import given, when, then
from iso8601 import parse_date

class DateTimeEncoder(json.JSONEncoder):
  '''Custom JSON Encoder to handle datetime objects

  from:
     `http://stackoverflow.com/questions/12122007/python-json-encoder-to-support-datetime`_
  also consider:
     `http://hg.tryton.org/2.4/trytond/file/ade5432ac476/trytond/protocols/jsonrpc.py#l53`_
  '''
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return obj.isoformat('T')
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
      return (datetime.datetime.min + obj).time().isoformat('T')
    else:
      return super(DateTimeEncoder, self).default(obj)
 
def get_json_response(context):
  if not hasattr(context, 'json'):
    context.json = context.response.json()
  return context.json

@given('an example "{resource_type}"')
def example_resource(context, resource_type):
  resource_factory = globals()['{}Factory'.format(resource_type)]
  context.example_resource = resource_factory()

@when('the example "{resource_type}" is POSTed to the "{collection}"')
def post_example_resource(context, resource_type, collection):
  #For **some** reason, I can't import this at the module level in a steps file
  import requests
  data = json.dumps(
      {resource_type.lower(): context.example_resource},
      cls=DateTimeEncoder,
      )
  context.response = requests.post(
      context.base_url+collection,
      data=data,
      headers={
        'Content-Type': 'application/json',
        },
      )

@then('a 201 status code is received')
def validate_status_201(context):
  assert context.response.status_code == 201

@then('the response has a Location header')
def validate_location_header(context):
  assert 'Location' in context.response.headers

@then('we receive a valid "{resource_type}" in the entity body')
def validate_resource_in_response(context, resource_type):
  assert 'application/json' == context.response.headers['Content-Type']
  assert resource_type.lower() in get_json_response(context)
  #FIXME more more more

@then('the received "{resource_type}" matches the one we posted')
def check_resource_equality_for_response(context, resource_type):
  root = unicode(resource_type.lower())
  resp_json = get_json_response(context)[root]
  orig_json = context.example_resource
  for k in orig_json:
    original = context.example_resource[k]
    response = resp_json[unicode(k)]
    if isinstance(original, datetime.datetime):
      response = parse_date(response)
    elif isinstance(original, datetime.date):
      response = datetime.datetime.strptime(response, '%Y-%m-%d').date()
    assert original == response, 'for {}: expected {}, received {}'.format(
        k, original, response)


# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

import datetime
from behave import given, when, then
from iso8601 import parse_date

from .utils import \
    Example, handle_example_resource, handle_named_example_resource, \
    set_property, get_resource, get_resource_table_singular, \
    get_service_endpoint_url, handle_get_resource_and_name_it, \
    handle_post_named_example_to_collection_endpoint, \
    handle_post_named_example, post_example, handle_get_example_resource

def get_json_response(context):
  if not hasattr(context, 'json'):
    context.json = context.response.json()
  return context.json

@given('an example "{resource_type}"')
def example_resource(context, resource_type):
  handle_example_resource(context, resource_type)

@given('a new "{resource_type}" named "{name}"')
def named_example_resource(context, resource_type, name, **kwargs):
  handle_named_example_resource(context, resource_type, name, **kwargs)

@given('"{name}" is POSTed to its collection')
def post_named_example_to_collection_endpoint(context, name):
  """Create a new resource for the given example. Expects that there is a
  `service_description` in `context` to use to lookup the endpoint url. The
  created resource is added to the context as the attribute name given by
  `name`.
  """
  handle_post_named_example_to_collection_endpoint(context, name)

@given('"{name}" is POSTed to "{url}"')
def post_named_example(context, name, url):
  handle_post_named_example(context, name, url)

@when('the example "{resource_type}" is POSTed to its collection')
def post_example_resource_to_its_collection(context, resource_type):
  endpoint_url = get_service_endpoint_url(context, resource_type)
  post_example_resource(context, resource_type, endpoint_url)

@when('the example "{resource_type}" is POSTed to the "{collection}"')
def post_example_resource(context, resource_type, collection):
  context.response = post_example(
      context, resource_type, context.example_resource, collection)

@when('GET of "{url}" as "{name}"')
def get_resource_and_name_it(context, url, name):
  handle_get_resource_and_name_it(context, url, name)

@when('GET of the resource "{name}"')
def get_example_resource(context, name):
  handle_get_example_resource(context, name)

@then('a "{status_code}" status code is received')
def validate_status_code(context, status_code):
  assert context.response.status_code == int(status_code), \
      'Expecxted status code {0}, received {1}'.format(
          status_code, context.response.status_code)

@then('a 201 status code is received')
def validate_status_201(context):
  assert context.response.status_code == 201, \
      'Expected status code 201, received {0}'.format(
          context.response.status_code)

@then('the response has a Location header')
def validate_location_header(context):
  assert 'Location' in context.response.headers

@then('we receive a valid "{resource_type}" in the entity body')
def validate_resource_in_response(context, resource_type):
  assert 'application/json' == context.response.headers['Content-Type']
  assert get_resource_table_singular(resource_type) in get_json_response(context)
  #FIXME more more more

def dates_within_tolerance(original, response):
  floor = datetime.datetime(
      original.year, original.month, original.day, original.hour,
      original.minute, original.second, tzinfo=original.tzinfo)
  ceiling = floor + datetime.timedelta(seconds=1)
  return floor <= response <= ceiling

@then('the received "{resource_type}" matches the one we posted')
def check_resource_equality_for_response(context, resource_type):
  root = unicode(get_resource_table_singular(resource_type))
  resp_json = get_json_response(context)[root]
  orig_json = context.example_resource
  for k in orig_json:
    original = context.example_resource[k]
    response = resp_json[unicode(k)]
    if isinstance(original, datetime.datetime):
      response = parse_date(response)
      assert dates_within_tolerance(original, response), \
          'for {0}: expected {1}, received {2}'.format(
              k, original, response)
      return
    elif isinstance(original, datetime.date):
      response = datetime.datetime.strptime(response, '%Y-%m-%d').date()
    assert original == response, 'for {0}: expected {1}, received {2}'.format(
        k, original, response)

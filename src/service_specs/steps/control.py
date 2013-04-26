import json
import requests
from behave import *
from .factories import ControlFactory

def get_json_response(context):
  if not hasattr(context, 'json'):
    context.json = context.response.json()
  return context.json

@given('an example control')
def example_control(context):
  context.control = ControlFactory()

@when('the example control is POSTed')
def post_example_control(context):
  context.response = requests.post(
      context.base_url+'/api/controls',
      data=json.dumps({'control': context.control}),
      headers={
        'Content-Type': 'application/json',
        },
      )

@then('a 201 status code is received')
def validate_status_201(context):
  assert context.response.status_code == 201

@then('the response has a Location header')
def get_control(context):
  assert 'Location' in context.response.headers

@then('we receive a valid control in the entity body')
def validate_control(context):
  assert 'application/json' == context.response.headers['Content-Type']
  assert 'control' in get_json_response(context)

@then('the received control matches the one we posted')
def check_control_equality(context):
  resp_json = get_json_response(context)[u'control']
  for k in context.control:
    assert context.control[k] == resp_json[unicode(k)]

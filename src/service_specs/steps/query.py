# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

@when('Querying "{resource_type}" with "{querystring}"')
def query_resource_collection(context, resource_type, querystring):
  url = '{0}?{1}'.format(
      get_service_endpoint_url(context, resource_type),
      querystring)
  get_resource_and_name_it(context, url, 'queryresultcollection')

@when('Querying "{resource_type}" with bad argument "{querystring}"')
def query_with_bad_argument(context, resource_type, querystring):
  url = '{0}?{1}'.format(
      get_service_endpoint_url(context, resource_type),
      querystring)
  context.response = get_resource(context, url)

@when('Querying "{resource_type}" with expression "{property_path}" equals literal "{value}"')
def query_resource_collection_with_literal(
    context, resource_type, property_path, value):
  value = eval(value)
  query_resource_collection(
      context, resource_type, '{0}={1}'.format(property_path, value))

def check_for_resource_in_queryresult(context, resource_name, expected):
  resource = getattr(context, resource_name)
  queryresult = context.queryresultcollection
  root = queryresult.keys()[0]
  from ggrc import models
  model_class = getattr(models, resource.resource_type)
  entry_list = queryresult[root][model_class.__tablename__]
  result_pairs = set([(o[u'id'], o[u'selfLink']) for o in entry_list])
  check_pair = (resource.get(u'id'), resource.get(u'selfLink'))
  if expected:
    assert check_pair in result_pairs, \
        'Expected to find {0} in results {1}'.format(
            check_pair, result_pairs)
  else:
    assert check_pair not in result_pairs, \
        'Expected not to find {0} in results {1}'.format(
            check_pair, result_pairs)


@then('"{resource_name}" is in query result')
def check_resource_in_queryresult(context, resource_name):
  check_for_resource_in_queryresult(context, resource_name, True)

@then('"{resource_name}" is not in query result')
def check_resource_not_in_queryresult(context, resource_name):
  check_for_resource_in_queryresult(context, resource_name, False)

@then('query result selfLink query string is "{expected_querystring}"')
def check_query_selfLink(context, expected_querystring):
  queryresult = context.queryresultcollection
  root = queryresult.keys()[0]
  selfLink = queryresult[root]['selfLink']
  idx = selfLink.find('?')
  assert selfLink[idx+1:] == expected_querystring, \
      'Expected to find query string {0}, found {1}'.format(
          expected_querystring, selfLink[idx+1:])

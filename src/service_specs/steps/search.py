
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from .utils import \
    handle_named_example_resource, get_service_endpoint_url, \
    handle_get_resource_and_name_it, handle_get_example_resource, \
    handle_post_named_example_to_collection_endpoint

@given('the following resources are POSTed')
def post_collection_of_resources(context):
  """Iterate over a table where the first two columns are `type` and `name`.
  Successive columns are for properties to be set on the resource before
  posting it to the relevant collection.
  """
  for row in context.table:
    resource_type = row[0]
    name = row[1]
    properties = dict([(heading, row[heading]) for heading in row.headings[2:]])
    handle_named_example_resource(context, resource_type, name, **properties)
    handle_post_named_example_to_collection_endpoint(context, name)
    handle_get_example_resource(context, name)

@when('fulltext search for "{terms}" as "{result_name}"')
def perform_search(context, terms, result_name):
  url = get_service_endpoint_url(context, 'search')
  handle_get_resource_and_name_it(
      context, url+'?q={0}'.format(terms), result_name)

@when('fulltext search grouped by type for "{terms}" as "{result_name}"')
def perform_grouped_search(context, terms, result_name):
  url = get_service_endpoint_url(context, 'search')
  handle_get_resource_and_name_it(
      context, url+'?q={0}&group_by_type=true'.format(terms), result_name)

def do_check_resource_is_in_result(
    context, resource_name, entry_list, expected=True):
  resource = getattr(context, resource_name)
  result_pairs = set([(o[u'id'], o[u'href']) for o in entry_list])
  check_pair = (resource.get(u'id'), resource.get(u'selfLink'))
  if expected:
    assert check_pair in result_pairs, \
        'Expected to find {0} in results {1}'.format(
            check_pair, result_pairs)
  else:
    assert check_pair not in result_pairs, \
        'Expected not to find {0} in results {1}'.format(
            check_pair, result_pairs)

def get_basic_result_list(context, result_name):
  result = getattr(context, result_name)
  return result['results']['entries']

def get_grouped_result_list(context, result_name, resource_type):
  result = getattr(context, result_name)
  return result['results']['entries'].get(resource_type, [])

@then('"{resource_name}" is in the search result "{result_name}"')
def check_resource_is_in_result(context, resource_name, result_name):
  entry_list = get_basic_result_list(context, result_name)
  do_check_resource_is_in_result(context, resource_name, entry_list, True)

@then('"{resource_name}" isn\'t in the search result "{result_name}"')
def check_resource_not_in_result(context, resource_name, result_name):
  entry_list = get_basic_result_list(context, result_name)
  do_check_resource_is_in_result(context, resource_name, entry_list, False)

@then('"{resource_name}" is in the "{group_name}" group of "{result_name}"')
def check_resource_in_result_group(
    context, resource_name, group_name, result_name):
  entry_list = get_grouped_result_list(context, result_name, group_name)
  do_check_resource_is_in_result(context, resource_name, entry_list, True)

@then('"{resource_name}" isn\'t in the "{group_name}" group of "{result_name}"')
def check_resource_not_in_result_group(
    context, resource_name, group_name, result_name):
  entry_list = get_grouped_result_list(context, result_name, group_name)
  do_check_resource_is_in_result(context, resource_name, entry_list, False)

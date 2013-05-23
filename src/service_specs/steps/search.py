@when('fulltext search for "{terms}" as "{result_name}"')
def perform_search(context, terms, result_name):
  url = get_service_endpoint_url(context, 'search')
  get_resource_and_name_it(context, url+'?q={0}'.format(terms), result_name)

def do_check_resource_is_in_result(
    context, resource_name, result_name, expected=True):
  resource = getattr(context, resource_name)
  result = getattr(context, result_name)
  result_pairs = set(
      [(o[u'id'], o[u'href']) for o in result['results']['entries']])
  check_pair = (resource.get(u'id'), resource.get(u'href'))
  if expected:
    assert check_pair in result_pairs, \
        'Expected to find {0} in results {1}'.format(
            check_pair, result_pairs)
  else:
    assert check_pair not in result_pairs, \
        'Expected not to find {0} in results {1}'.format(
            check_pair, result_pairs)

@then('"{resource_name}" is in the search result "{result_name}"')
def check_resource_is_in_result(context, resource_name, result_name):
  do_check_resource_is_in_result(context, resource_name, result_name, True)

@then('"{resource_name}" isn\'t in the search result "{result_name}"')
def check_resource_not_in_result(context, resource_name, result_name):
  do_check_resource_is_in_result(context, resource_name, result_name, False)

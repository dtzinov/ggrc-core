import json
from flask import request, current_app
from ggrc.fulltext import get_indexer
from .common import DateTimeEncoder
from .util import url_for

def search():
  terms = request.args.get('q')
  if not terms or terms is None:
    return current_app.make_response((
      'Query parameter "q" specifying search terms must be provided.',
      400,
      [('Content-Type', 'text/plain')],
      ))
  should_group_by_type = request.args.get('group_by_type')
  if should_group_by_type is not None and \
      should_group_by_type.lower() == 'true':
    return group_by_type_search(terms)
  return basic_search(terms)

def do_search(terms, list_for_type):
  indexer = get_indexer()
  results = indexer.search(terms)
  for result in results:
    id = result.key
    model_type = result.type
    entries_list = list_for_type(model_type)
    entries_list.append({
      'id': id,
      'type': model_type,
      'href': url_for(model_type, id=id),
      })

def make_search_result(entries):
  return current_app.make_response((
    json.dumps({ 'results': {
        'selfLink': request.url,
        'entries': entries,
        }
      }, cls=DateTimeEncoder),
    200,
    [('Content-Type', 'application/json')],
    ))

def basic_search(terms):
  entries = []
  list_for_type = lambda t: entries
  do_search(terms, list_for_type)
  return make_search_result(entries)

def group_by_type_search(terms):
  entries = {}
  list_for_type = \
      lambda t: entries[t] if t in entries else entries.setdefault(t, [])
  do_search(terms, list_for_type)
  return make_search_result(entries)

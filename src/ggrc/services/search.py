import json
from flask import request, current_app
from ggrc.fulltext import get_indexer
from .common import DateTimeEncoder
from .util import url_for

def perform_search():
  terms = request.args.get('q')
  #types = request.args.get('type')
  if not terms or terms is None:
    return current_app.make_response((
      'Query parameter "q" specifying search terms must be provided.',
      400,
      [('Content-Type', 'text/plain')],
      ))
  indexer = get_indexer()
  results = indexer.search(terms)
  entries = []
  for result in results:
    id = result.key
    model_type = result.type
    entries.append({
      'id': id,
      'type': model_type,
      'href': url_for(model_type, id),
      })
  return current_app.make_response((
    json.dumps({ 'results': {
        'selfLink': request.url,
        'entries': entries,
        }
      }, cls=DateTimeEncoder),
    200,
    [('Content-Type', 'application/json')],
    ))

import json
from flask.views import MethodView

class ServiceDescription(MethodView):
  def get(self):
    from ggrc import collections
    from ggrc import services
    endpoints = {}
    for context_path, service in collections:
      service = getattr(services, service.__name__)
      endpoints[service.__name__] = {
          'href': service.url_for(),
          #TODO additional fields
          #'discoveryVersion': '',
          #'id': '',
          #'name': '',
          #'version': '',
          #'title': '',
          #'description': '',
          #'documentationLink': '',
          }
    return json.dumps({
        'service_description': {
          'name': 'gGRC-Core',
          'endpoints': endpoints,
          #TODO additional fields
          #'id': '',
          #'title': '',
          #'description': '',
          #'documentationLink': '',
          },
        })

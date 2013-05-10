import json
from flask import request
from flask.views import MethodView

"""RESTful service discovery API for gGRC services."""

class ServiceDescription(MethodView):
  """Flask view providing a RESTful service discovery resource for all gGRC
  resources, resource collections and services.
  """
  def get(self):
    from ggrc import services
    endpoints = {}
    for context_path, service in services.all_collections():
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
          'selfLink': request.url,
          #TODO additional fields
          #'id': '',
          #'title': '',
          #'description': '',
          #'documentationLink': '',
          },
        })

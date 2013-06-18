# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

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
    for entry in services.all_collections():
      service = getattr(services, entry.model_class.__name__)
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
    endpoints['search'] = { 'href': '/search' }
    endpoints['log_event'] = {'href': '/api/log_event' }
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

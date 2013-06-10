# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from flask import request
from .common import Resource

class LogEvents(Resource):
  def modified_attr_name(self):
    return 'created_at'

  def dispatch_request(self, *args, **kwargs):
    method = request.method.lower()

    if method in ['head','get','post']:
      return super(LogEvents, self).dispatch_request(*args, **kwargs)

    raise NotImplementedError()

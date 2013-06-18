# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from flask import request, current_app

def log_event():
  '''Log javascript client errors to syslog via application logger.'''
  method = request.method.lower()
  if method == 'post':
    severity = request.json['log_event']['severity']
    description = request.json['log_event']['description']
    current_app.logger.error('Javascript Client: {0} {1}'.format(
      severity, description))
    return current_app.make_response(('', 200, []))
  raise NotImplementedError()


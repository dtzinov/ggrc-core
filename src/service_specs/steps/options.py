# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from .utils import handle_named_example_resource

@given('an Option named "{name}" with role "{role}"')
def create_option(context, name, role):
  handle_named_example_resource(context, 'Option', name, role=role)

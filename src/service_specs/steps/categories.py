# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from .utils import handle_named_example_resource

@given('a Category resource named "{name}" for scope "{scope}"')
def create_category(context, name, scope):
  handle_named_example_resource(context, 'Category', name, scope_id=int(scope))

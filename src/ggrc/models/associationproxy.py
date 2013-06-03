
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

from sqlalchemy.ext.associationproxy \
    import association_proxy as orig_association_proxy

"""Wrapper for SQLAlchemy association proxies. Automatically add creator
function for model classes for join table associations.
"""

def resolve_class(model_class):
  if type(model_class) is str:
    import ggrc.models
    return getattr(ggrc.models, model_class)
  return model_class

def association_proxy(target_collection, attr, model_class):
  """Return an association proxy with a creator function specified."""
  #FIXME is model_class needed? can't that be determined off of reflection?!
  return orig_association_proxy(target_collection, attr, creator=\
      lambda arg: resolve_class(model_class)(**{
        attr: arg,
        'modified_by_id': 1, #FIXME
        }))
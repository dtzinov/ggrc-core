# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from collections import namedtuple
from flask import session
from ggrc.login import get_current_user
from .user_permissions import UserPermissions

Permission = namedtuple('Permission', 'action resource_type context_id')

class DefaultUserPermissionsProvider(object):
  def __init__(self, settings):
    pass

  def permissions_for(self, user):
    return DefaultUserPermissions()

class DefaultUserPermissions(UserPermissions):
  def _is_allowed(self, permission):
    if 'permissions' not in session:
      return False
    permissions = session['permissions']
    if permissions is None:
      return True
    return permission.context_id in \
        permissions\
          .get(permission.action, {})\
          .get(permission.resource_type, ())

  def is_allowed_create(self, resource_type, context_id):
    """Whether or not the user is allowed to create a resource of the specified
    type in the context."""
    return self._is_allowed(Permission('create', resource_type, context_id))

  def is_allowed_read(self, resource_type, context_id):
    """Whether or not the user is allowed to read a resource of the specified
    type in the context."""
    return self._is_allowed(Permission('read', resource_type, context_id))

  def is_allowed_update(self, resource_type, context_id):
    """Whether or not the user is allowed to update a resource of the specified
    type in the context."""
    return self._is_allowed(Permission('update', resource_type, context_id))

  def is_allowed_delete(self, resource_type, context_id):
    """Whether or not the user is allowed to delete a resource of the specified
    type in the context."""
    return self._is_allowed(Permission('delete', resource_type, context_id))

  def _get_contexts_for(self, action, resource_type):
    if 'permissions' not in session:
      return False
    permissions = session['permissions']
    if permissions is None:
      return None
    ret = list(permissions.get(action, {}).get(resource_type, ()))
    ret.append(None)
    return ret

  def create_contexts_for(self, resource_type):
    """All contexts in which the user has create permission."""
    return self._get_contexts_for('create', resource_type)

  def read_contexts_for(self, resource_type):
    """All contexts in which the user has read permission."""
    return self._get_contexts_for('read', resource_type)

  def update_contexts_for(self, resource_type):
    """All contexts in which the user has update permission."""
    return self._get_contexts_for('update', resource_type)

  def delete_contexts_for(self, resource_type):
    """All contexts in which the user has delete permission."""
    return self._get_contexts_for('delete', resource_type)


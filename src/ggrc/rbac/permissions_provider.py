# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from .user_permissions import UserPermissions

class DefaultUserPermissionsProvider(object):
  def __init__(self, settings):
    pass

  def permissions_for(self, user):
    return DefaultUserPermissions()

class DefaultUserPermissions(UserPermissions):
  def is_allowed_create(self, resource_type, context_id):
    """Whether or not the user is allowed to create a resource of the specified
    type in the context."""
    return True

  def is_allowed_read(self, resource_type, context_id):
    """Whether or not the user is allowed to read a resource of the specified
    type in the context."""
    return True

  def is_allowed_update(self, resource_type, context_id):
    """Whether or not the user is allowed to update a resource of the specified
    type in the context."""
    return True

  def is_allowed_delete(self, resource_type, context_id):
    """Whether or not the user is allowed to delete a resource of the specified
    type in the context."""
    return True

  def create_contexts_for(self, resource_type):
    """All contexts in which the user has create permission."""
    return None

  def read_contexts_for(self, resource_type):
    """All contexts in which the user has read permission."""
    return None

  def update_contexts_for(self, resource_type):
    """All contexts in which the user has update permission."""
    return None

  def delete_contexts_for(self, resource_type):
    """All contexts in which the user has delete permission."""
    return None


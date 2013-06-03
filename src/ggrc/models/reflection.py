
# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By:
# Maintained By:

"""Utilties to deal with introspecting gGRC models for publishing, creation,
and update from resource format representations, such as JSON."""

class DontPropagate(object):
  """Attributes wrapped by ``DontPropagate`` instances should not be considered
  to be a part of an inherited list. For example, ``_update_attrs`` can be
  inherited from ``_publish_attrs`` if left unspecified. This class provides
  a mechanism to use that inheritance while excluding some elements from the
  resultant inherited list. For example, this:

  .. sourcecode::

    _publish_attrs = [
      'inherited_attr',
      DontPropagate('not_inherited_attr'),
      ]

  is equivalent to this:

  .. sourcecode::

    _publish_attrs = [
    'inherited_attr',
    'not_inherited_attr',
    ]
    _update_attrs = [
    'inherited_attr',
    ]
  """
  def __init__(self, attr_name):
    self.attr_name = attr_name

class PublishOnly(DontPropagate):
  """Alias of ``DontPropagate`` for use in a ``_publish_attrs`` specification.
  """
  pass

class AttributeInfo(object):
  """Gather model CRUD information by reflecting on model classes. Builds and
  caches a list of the publishing properties for a class by walking the
  class inheritance tree.
  """
  def __init__(self, tgt_class):
    self._publish_attrs = AttributeInfo.gather_publish_attrs(tgt_class)
    self._update_attrs = AttributeInfo.gather_update_attrs(tgt_class)
    self._create_attrs = AttributeInfo.gather_create_attrs(tgt_class)

  @classmethod
  def gather_attrs(cls, tgt_class, src_attrs, accumulator=None):
    """Gathers the attrs to be included in a list for publishing, update, or
    some other purpose. Supports inheritance by iterating the list of
    ``src_attrs`` until a list is found.

    Inheritance of some attributes can be circumvented through use of the
    ``DontPropoagate`` decorator class.
    """
    src_attrs = src_attrs if type(src_attrs) is list else [src_attrs]
    accumulator = accumulator if accumulator is not None else set()
    ignore_dontpropagate = True
    for attr in src_attrs:
      attrs = tgt_class.__dict__.get(attr, None)
      if attrs is not None:
        if not ignore_dontpropagate:
          attrs = [a for a in attrs if not isinstance(a, DontPropagate)]
        else:
          attrs = [a if not isinstance(a, DontPropagate) else a.attr_name for \
              a in attrs]
        accumulator.update(attrs)
        break
      else:
        ignore_dontpropagate = False
    for base in tgt_class.__bases__:
      cls.gather_attrs(base, src_attrs, accumulator)
    return accumulator

  @classmethod
  def gather_publish_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, '_publish_attrs')

  @classmethod
  def gather_update_attrs(cls, tgt_class):
    attrs = cls.gather_attrs(tgt_class, ['_update_attrs', '_publish_attrs'])
    return attrs

  @classmethod
  def gather_create_attrs(cls, tgt_class):
    return cls.gather_attrs(tgt_class, [
      '_create_attrs', '_update_attrs', '_publish_attrs'])